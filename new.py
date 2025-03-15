import sys
import sqlite3
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTableWidget, QTableWidgetItem, QLineEdit,
    QLabel, QFormLayout, QDialog, QMessageBox, QCheckBox, QSpinBox
)


# Database setup
def initialize_db():
    conn = sqlite3.connect("pos_database.db")
    cursor = conn.cursor()

    # Inventory Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bike_name TEXT,
                        bike_model TEXT,
                        chassis_no TEXT,
                        reg_no TEXT UNIQUE,
                        purchase_price REAL,
                        purchase_from TEXT,
                        client_mobile TEXT,
                        client_cnic TEXT,
                        purchase_date TEXT,
                        product_status TEXT DEFAULT 'Purchased')''')
    
    # User Management Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    client_name TEXT,
                    client_cnic TEXT,
                    client_mobile TEXT,
                    reg_no TEXT UNIQUE,
                    product_status TEXT,
                    purchase_date TEXT,
                    sale_date TEXT,
                    payment_method TEXT)''')
    
     # Sales Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        client_cnic TEXT,
                        client_mobile TEXT,
                        reg_no TEXT UNIQUE,
                        sale_price REAL,
                        purchase_date TEXT,
                        sale_date TEXT,
                        payment_method TEXT,
                        duration INTEGER,
                        advance_payment REAL,
                        monthly_installment REAL,
                        profit REAL,
                        product_status TEXT DEFAULT 'Sold')''')
    
    conn.commit()
    conn.close()

# Home Page
class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bismillah Moters - Home")
        self.setGeometry(100, 100, 500, 400)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Main layout is vertical to include the header at the top
        main_layout = QVBoxLayout(central_widget)

        # Header label
        header = QLabel("BISMILLAH MOTERS")
        header_font = QFont('Arial', 42, QFont.Weight.Bold)  # Reduced font size from 24 to 18
        header.setFont(header_font)
        header.setStyleSheet("background-color: green; color: white; padding: 10px;")  # Reduced padding
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Button styling
        button_style = """
        QPushButton {
            font: bold 14px;
            border: 2px solid #555;
            border-radius: 10px;
            padding: 5px;
            background-color: white;
            min-width: 80px;
        }
        QPushButton:hover {
            background-color: #3366cc;
            border-style: solid;
        }
        """

        # Adding buttons
        self.inventory_button = QPushButton("Inventory Management")
        self.inventory_button.setStyleSheet(button_style)
        self.inventory_button.clicked.connect(self.open_inventory_page)
        buttons_layout.addWidget(self.inventory_button)

        self.user_management_button = QPushButton("User Management")
        self.user_management_button.setStyleSheet(button_style)
        self.user_management_button.clicked.connect(self.open_user_management_page)
        buttons_layout.addWidget(self.user_management_button)

        self.sales_button = QPushButton("Sales Management")
        self.sales_button.setStyleSheet(button_style)
        self.sales_button.clicked.connect(self.open_sales_page)
        buttons_layout.addWidget(self.sales_button)

        # Add buttons layout to main layout
        main_layout.addLayout(buttons_layout)

    def open_inventory_page(self):
        self.inventory_page = InventoryPage()
        self.inventory_page.show()

    def open_user_management_page(self):
        self.user_management_page = UserManagementPage()
        self.user_management_page.show()

    def open_sales_page(self):
        self.sales_page = SalesPage()
        self.sales_page.show()



        
# Sales Management Page
class SalesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Management")
        self.setGeometry(200, 200, 900, 500)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels(["Client Name", "CNIC", "Mobile No", "Bike Reg No", "Sale Price", "Purchase Date", "Sale Date", "Payment Method", "Duration", "Advance Payment", "Monthly Installment", "Profit", "Status"])
        layout.addWidget(self.table)

        self.new_sale_button = QPushButton("New Sale")
        self.new_sale_button.clicked.connect(self.open_new_sale_dialog)
        layout.addWidget(self.new_sale_button)

        self.delete_button = QPushButton("Delete Selected Sale")
        self.delete_button.clicked.connect(self.delete_selected_sale)
        layout.addWidget(self.delete_button)

        self.load_sales()
        self.setLayout(layout)

    def load_sales(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT client_name, client_cnic, client_mobile, reg_no, sale_price, purchase_date, sale_date, payment_method, duration, advance_payment, monthly_installment, profit, product_status FROM sales")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def delete_sale(self, reg_no):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales WHERE reg_no = ?", (reg_no,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Sale record deleted successfully!")
        self.load_sales()

    def delete_selected_sale(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            reg_no = self.table.item(selected_row, 3).text()
            self.delete_sale(reg_no)
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a sale record to delete!")

    def open_new_sale_dialog(self):
        dialog = NewSaleDialog(self)
        if dialog.exec():
            self.load_sales()

class NewSaleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Sale Entry")
        self.setGeometry(300, 200, 400, 350)
        layout = QFormLayout()

        self.client_name = QLineEdit()
        self.client_cnic = QLineEdit()
        self.client_mobile = QLineEdit()

        self.reg_no_search = QLineEdit()
        self.reg_no_search.setPlaceholderText("Enter Bike Reg No")
        self.reg_no_search.textChanged.connect(self.search_reg_no)
        self.purchase_price = QLineEdit()
        self.purchase_price.setReadOnly(True)
        self.sale_price = QLineEdit()
        self.sale_price.textChanged.connect(self.update_profit)
        self.profit = QLineEdit()
        self.profit.setReadOnly(True)

        self.payment_method = QCheckBox("On Installment")
        self.payment_method.stateChanged.connect(self.toggle_installment_fields)
        self.duration = QSpinBox()
        self.duration.setRange(1, 12)
        self.duration.setEnabled(False)
        self.advance_payment = QLineEdit()
        self.advance_payment.setEnabled(False)
        self.monthly_installment = QLineEdit()
        self.monthly_installment.setReadOnly(True)
        self.advance_payment.textChanged.connect(self.update_installment)

        self.submit_button = QPushButton("Add New Sale")
        self.submit_button.clicked.connect(self.submit_sale)

        layout.addRow("Client Name:", self.client_name)
        layout.addRow("Client CNIC:", self.client_cnic)
        layout.addRow("Client Mobile:", self.client_mobile)
        layout.addRow("Bike Reg No:", self.reg_no_search)
        layout.addRow("Purchase Price:", self.purchase_price)
        layout.addRow("Sale Price:", self.sale_price)
        layout.addRow("Profit:", self.profit)
        layout.addRow(self.payment_method)
        layout.addRow("Duration (months):", self.duration)
        layout.addRow("Advance Payment:", self.advance_payment)
        layout.addRow("Monthly Installment:", self.monthly_installment)
        layout.addRow(self.submit_button)
        
        self.setLayout(layout)

    def submit_sale(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        reg_no = self.reg_no_search.text()
        client_name = self.client_name.text()
        client_cnic = self.client_cnic.text()
        client_mobile = self.client_mobile.text()
        sale_price = self.sale_price.text()
        payment_method = "Installments" if self.payment_method.isChecked() else "Net Cash"
        
        cursor.execute("SELECT purchase_price, purchase_date FROM inventory WHERE reg_no = ?", (reg_no,))
        record = cursor.fetchone()
        if not record:
            QMessageBox.warning(self, "Database Error", "Bike registration number not found!")
            conn.close()
            return

        purchase_price, purchase_date = record
        profit = float(sale_price) - float(purchase_price)
        sale_date = QDate.currentDate().toString("yyyy-MM-dd")

        # Insert into sales table
        if payment_method == "Installments":
            duration = self.duration.value()
            advance_payment = float(self.advance_payment.text())
            monthly_installment = float(self.monthly_installment.text())
            cursor.execute("""
                INSERT INTO sales (client_name, client_cnic, client_mobile, reg_no, sale_price, purchase_date, sale_date, payment_method, duration, advance_payment, monthly_installment, profit, product_status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Sold')
            """, (client_name, client_cnic, client_mobile, reg_no, sale_price, purchase_date, sale_date, payment_method, duration, advance_payment, monthly_installment, profit))
        else:
            cursor.execute("""
                INSERT INTO sales (client_name, client_cnic, client_mobile, reg_no, sale_price, purchase_date, sale_date, payment_method, profit, product_status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Sold')
            """, (client_name, client_cnic, client_mobile, reg_no, sale_price, purchase_date, sale_date, payment_method, profit))

        # Update users table
        cursor.execute("SELECT id FROM users WHERE reg_no = ? AND product_status = 'Purchased'", (reg_no,))
        if cursor.fetchone():
            # If already purchased, update to sold if not already
            cursor.execute("UPDATE users SET client_name=?, client_cnic=?, client_mobile=?, product_status='Sold', sale_date=?, payment_method=? WHERE reg_no=? AND product_status = 'Purchased'",
                        (client_name, client_cnic, client_mobile, sale_date, payment_method, reg_no))
        else:
            # Insert new user record if not exist
            cursor.execute("INSERT INTO users (client_name, client_cnic, client_mobile, reg_no, product_status, purchase_date, sale_date, payment_method) VALUES (?, ?, ?, ?, 'Sold', ?, ?, ?)", 
                        (client_name, client_cnic, client_mobile, reg_no, purchase_date, sale_date, payment_method))
        conn.commit()
        QMessageBox.information(self, "Success", "Sale record added successfully!")
        self.accept()
        conn.close()




    def load_inventory(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT reg_no, purchase_price FROM inventory WHERE product_status='Purchased'")
        records = cursor.fetchall()
        conn.close()
        self.inventory_data = {record[0]: record[1] for record in records}
        self.reg_no.addItems(self.inventory_data.keys())

    def filter_reg_no(self):
        text = self.search_reg_no.text().lower()
        self.reg_no.clear()
        self.reg_no.addItem("Select Reg No")
        for reg in self.inventory_data.keys():
            if text in reg.lower():
                self.reg_no.addItem(reg)

    def update_purchase_price(self):
        selected_reg_no = self.reg_no.currentText()
        if selected_reg_no in self.inventory_data:
            self.purchase_price.setText(str(self.inventory_data[selected_reg_no]))

    def update_profit(self):
        if self.sale_price.text() and self.purchase_price.text():
            self.profit.setText(str(float(self.sale_price.text()) - float(self.purchase_price.text())))
            
    def toggle_installment_fields(self):
        enabled = self.payment_method.isChecked()
        self.duration.setEnabled(enabled)
        self.advance_payment.setEnabled(enabled)

    def update_profit(self):
        if self.sale_price.text() and self.purchase_price.text():
            self.profit.setText(str(float(self.sale_price.text()) - float(self.purchase_price.text())))

    def search_reg_no(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT purchase_price FROM inventory WHERE reg_no = ?", (self.reg_no_search.text(),))
        result = cursor.fetchone()
        conn.close()
        if result:
            self.purchase_price.setText(str(result[0]))
        else:
            self.purchase_price.clear()   

    def update_installment(self):
        if self.sale_price.text() and self.advance_payment.text():
            remaining = float(self.sale_price.text()) - float(self.advance_payment.text())
            self.monthly_installment.setText(str(round(remaining / self.duration.value(), 2)))
 
# Inventory Management Page
class InventoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(200, 200, 700, 400)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Bike Name", "Bike Model", "Chassis No", "Reg No", "Purchase Price", "Purchase From", "Purchase Date", "Mobile No", "CNIC", "Status"])
        layout.addWidget(self.table)

        self.add_button = QPushButton("Add New Inventory")
        self.add_button.clicked.connect(self.open_add_inventory_dialog)
        layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete Selected Inventory")
        self.delete_button.clicked.connect(self.delete_selected_inventory)
        layout.addWidget(self.delete_button)

        self.load_inventory()
        self.setLayout(layout)

    def load_inventory(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT bike_name, bike_model, chassis_no, reg_no, purchase_price, purchase_from, purchase_date, client_mobile, client_cnic, product_status FROM inventory")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def open_add_inventory_dialog(self):
        dialog = AddInventoryDialog(self)
        dialog.exec()
        self.load_inventory()

    def delete_selected_inventory(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            reg_no = self.table.item(selected_row, 3).text()
            conn = sqlite3.connect("pos_database.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inventory WHERE reg_no = ?", (reg_no,))
            conn.commit()
            conn.close()
            self.load_inventory()
        else:
            QMessageBox.warning(self, "Warning", "Please select a row to delete.")
            
            

# Add Inventory Dialog
class AddInventoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Inventory")
        self.setGeometry(300, 300, 400, 300)
        layout = QFormLayout()

        self.bike_name = QLineEdit()
        self.bike_model = QLineEdit()
        self.chassis_no = QLineEdit()
        self.reg_no = QLineEdit()
        self.purchase_price = QLineEdit()
        self.purchase_from = QLineEdit()
        self.client_mobile = QLineEdit()
        self.client_cnic = QLineEdit()

        layout.addRow("Bike Name:", self.bike_name)
        layout.addRow("Bike Model:", self.bike_model)
        layout.addRow("Chassis No:", self.chassis_no)
        layout.addRow("Reg No:", self.reg_no)
        layout.addRow("Purchase Price:", self.purchase_price)
        layout.addRow("Purchase From:", self.purchase_from)
        layout.addRow("Client Mobile:", self.client_mobile)
        layout.addRow("Client CNIC:", self.client_cnic)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_inventory)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_inventory(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        current_date = QDate.currentDate().toString("yyyy-MM-dd")  # Get current date in the format YYYY-MM-DD
        try:
            cursor.execute("INSERT INTO inventory (bike_name, bike_model, chassis_no, reg_no, purchase_price, purchase_from, purchase_date, client_mobile, client_cnic, product_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Purchased')", 
                           (self.bike_name.text(), self.bike_model.text(), self.chassis_no.text(), self.reg_no.text(), self.purchase_price.text(), self.purchase_from.text(), current_date, self.client_mobile.text(), self.client_cnic.text()))
            cursor.execute("INSERT INTO users (client_name, client_cnic, client_mobile, reg_no, product_status, purchase_date, sale_date, payment_method) VALUES (?, ?, ?, ?, 'Purchased', ?, NULL, 'Net Cash')", 
                           (self.purchase_from.text(), self.client_cnic.text(), self.client_mobile.text(), self.reg_no.text(), current_date))
            conn.commit()
            QMessageBox.information(self, "Success", "Inventory added successfully!")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Database Error", str(e))
        finally:
            conn.close()


        
        

# User Management Page
class UserManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(200, 200, 700, 400)
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(8)  # Ensure you have the correct column count
        self.table.setHorizontalHeaderLabels(["Client Name", "CNIC", "Mobile No", "Bike Reg No", "Status", "Purchase Date", "Sale Date", "Payment Method"])
        layout.addWidget(self.table)

        self.delete_button = QPushButton("Delete Selected User")
        self.delete_button.clicked.connect(self.delete_selected_user)
        layout.addWidget(self.delete_button)

        self.load_users()
        self.setLayout(layout)

    def load_users(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT client_name, client_cnic, client_mobile, reg_no, product_status, purchase_date, sale_date, payment_method FROM users")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data) if col_data else ""))

    def delete_selected_user(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Selection Error", "Please select a user to delete!")
            return

        reg_no = self.table.item(selected_row, 3).text()  # Assuming 'reg_no' is in column index 3
        reply = QMessageBox.question(self, 'Delete Confirmation', 'Are you sure you want to delete this user?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.delete_user(reg_no)


    def delete_user(self, reg_no):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()

        try:
            # Optionally delete from sales or inventory if needed
            cursor.execute("DELETE FROM sales WHERE reg_no = ?", (reg_no,))
            cursor.execute("DELETE FROM inventory WHERE reg_no = ?", (reg_no,))
            cursor.execute("DELETE FROM users WHERE reg_no = ?", (reg_no,))
            conn.commit()
            QMessageBox.information(self, "Success", "User deleted successfully!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Failed to delete user: {e}")
        finally:
            conn.close()
        self.load_users()  # Refresh the list



if __name__ == "__main__":
    initialize_db()
    app = QApplication(sys.argv)
    mainWin = HomePage()
    mainWin.show()
    sys.exit(app.exec())
