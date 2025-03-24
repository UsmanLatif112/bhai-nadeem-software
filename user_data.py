import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QHBoxLayout, QLabel, QLineEdit, QHeaderView, QApplication, QDialog, QFormLayout,QDateEdit, QCheckBox, QComboBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QFont

class UserPage(QWidget):
    def __init__(self,user_id,invertr_id):
        super().__init__()
        self.user_id = user_id
        self.invertr_id = invertr_id 
        self.setWindowTitle("Sales Management")
        self.setGeometry(200, 200, 900, 500)
        self.connection = sqlite3.connect("pos_database.db")
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        header_widget = self.create_header()
        self.layout.addWidget(header_widget)
        self.search_bar_layout = self.create_search_bar()
        self.layout.addLayout(self.search_bar_layout)

        self.table = self.setup_table()
        self.layout.addWidget(self.table)

        button_bar_layout = self.create_button_bar()
        self.layout.addLayout(button_bar_layout)
        self.load_sales()

    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)

        logo_label = QLabel()
        logo_pixmap = QPixmap("BM_moters.png")
        logo_label.setPixmap(logo_pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation))
        header_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)

        header_text = QLabel("Sales Management")
        header_text.setStyleSheet("color: white;")
        header_text.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_layout.addStretch(1)
        header_layout.addWidget(header_text, 0, Qt.AlignmentFlag.AlignVCenter)
        header_layout.addStretch(1)

        return header_widget

    def create_search_bar(self):
        layout = QHBoxLayout()
        layout.addStretch(1)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Sales...")
        self.search_input.setFont(QFont("Arial", 10))
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: #004d00;
                border: 2px solid #004d00;
                border-radius: 10px;
                padding: 5px 10px;
            }
        """)
        self.search_input.setFixedHeight(30)
        self.search_input.setFixedWidth(200)
        self.search_input.textChanged.connect(self.load_sales)
        layout.addWidget(self.search_input)

        layout.setContentsMargins(0, 0, 20, 0)

        return layout

    def create_button_bar(self):
        layout = QHBoxLayout()
        layout.addStretch(1)

        self.add_sale_button = QPushButton("Print")
        self.add_sale_button.clicked.connect(self.open_new_sale_dialog)
        self.add_sale_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #004d00;
                border: 2px solid #004d00;
                border-radius: 10px;
                padding: 5px;
                font-size: 13px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #c8ffc8;
            }
        """)
        self.add_sale_button.setFixedSize(200, 30)
        layout.addWidget(self.add_sale_button)

        self.delete_button = QPushButton("Delete Selected Sale")
        self.delete_button.clicked.connect(self.delete_selected_sale)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #004d00;
                border: 2px solid #004d00;
                border-radius: 10px;
                padding: 5px;
                font-size: 13px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #c8ffc8;
            }
        """)
        self.delete_button.setFixedSize(200, 30)
        layout.addWidget(self.delete_button)

        layout.setContentsMargins(0, 0, 20, 20)

        return layout

    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(15)  # Increase column count by one for the checkbox
        table.setHorizontalHeaderLabels([
            "Select", "Client Name", "Client Mobile No", "Client CNIC", "Bike Chassis No", "Purchase Price", "Sale Price", 
            "Date","Product Status", "Payment Method", "Remaining Amount", "Duration", "Advance Payment", "Monthly Installment", "Action"
        ])
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #004d00;
                font-size: 14px;
                color: black;
                margin: 10px;
            }
            QHeaderView::section {
                background-color: #004d00;
                color: white;
                font-weight: bold;
            }
        """)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        return table


    def load_sales(self):
        """ Fetch product details from the sales table based on user_id and display them in the frontend table. """
        self.connection = sqlite3.connect("pos_database.db")
        cursor = self.connection.cursor()
        if self.user_id:
            cursor.execute("SELECT client_cnic FROM sales WHERE id = ?", (self.user_id,))
            result = cursor.fetchone()
            if result:
                client_cnic = result[0]
        if self.invertr_id:  # If no CNIC found in sales, check inventory
            cursor.execute("SELECT client_cnic FROM inventory WHERE id = ?", (self.invertr_id,))
            result = cursor.fetchone()
            if result:
                client_cnic = result[0]

        if not client_cnic:
            return

        # Fetch data from both tables based on client_cnic
        query_sales = """
            SELECT client_name, client_mobile,client_cnic, chassis_no, 'None' AS purchase_price, sale_price,
                 sale_date,product_status, payment_method,remaining_amount, duration, advance_payment, 
                monthly_installment
            FROM sales
            WHERE client_cnic = ?
        """
        
        query_inventory = """
            SELECT client_name,client_mobile,client_cnic, chassis_no,purchase_price,'None' AS sale_price, purchase_date,product_status,'None' AS payment_method,'None' AS remaining_amount, 'None' AS duration, 'None' AS advance_payment, 
            'None' AS monthly_installment

            FROM inventory
            WHERE client_cnic = ?
        """

        cursor.execute(query_sales, (client_cnic,))
        records_sales = cursor.fetchall()
        cursor.execute(query_inventory, (client_cnic,))
        records_inventory = cursor.fetchall()
        all_records = records_sales + records_inventory 
        self.table.setRowCount(0)  
        if all_records:
            self.table.setRowCount(len(all_records)) 
            for row_idx, row_data in enumerate(all_records):
                # import pdb;pdb.set_trace()
                checkbox = QTableWidgetItem()
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                self.table.setItem(row_idx, 0, checkbox)

                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.table.setItem(row_idx, col_idx + 1, item)
                if row_data[8] not in [None,'None','']:
                    manage_btn = QPushButton("Manage")
                    manage_btn.clicked.connect(lambda _, sale_id=row_data[3] : self.open_new_sale_dialog(sale_id))
                    self.table.setCellWidget(row_idx, 14, manage_btn)

        else:
            QMessageBox.information(self, "No Sales Found", "No sales records found for this user.")

        self.connection.close()

    def delete_selected_sale(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            chassis_no = self.table.item(selected_row, 3).text()
            self.delete_sale(chassis_no)

    def delete_sale(self, chassis_no):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales WHERE chassis_no = ?", (chassis_no,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Sale record deleted successfully!")
        self.load_sales()

    def open_new_sale_dialog(self,row_id):
        # import pdb;pdb.set_trace()
        connection = sqlite3.connect("pos_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT chassis_no,monthly_installment,duration,remaining_amount FROM sales WHERE chassis_no = ?", (row_id,))
        result = cursor.fetchone()
        connection.close()

        chassis_no = result[0]
        monthly_installment = result[1]
        duration = result[2]
        remaining_amount = result[3]
        dialog = NewSaleDialog(chassis_no, monthly_installment, duration, remaining_amount, parent=self)
        dialog.exec()
        # import pdb;pdb.set_trace()
        # self.load_sales()

class NewSaleDialog(QDialog):
    def __init__(self, chassis_no, monthly_installment, duration, remaining_amount, parent=None):
        super().__init__(parent)  # Correctly initialize QDialog
        self.setWindowTitle("Update Payments")
        self.setGeometry(300, 300, 400, 200)
        layout = QFormLayout(self)

        # Create input fields
        self.chassis_no = QLineEdit()
        self.chassis_no.setText(chassis_no)
        self.chassis_no.setReadOnly(True)

        self.duration = QComboBox()
        self.duration.addItems([str(i) for i in range(1, 13)])  # 1 to 12 months
        self.duration.setCurrentText(str(duration))

        self.monthly_installment = QLineEdit()
        self.monthly_installment.setText(str(monthly_installment))
        self.monthly_installment.setReadOnly(True)

        self.remaining_amount = QLineEdit()
        self.remaining_amount.setText(str(remaining_amount))
        self.remaining_amount.setReadOnly(True)

        self.payment_no = QLineEdit()

        # Add fields to layout
        layout.addRow("Chassis No:", self.chassis_no)
        layout.addRow("Duration (Months):", self.duration)
        layout.addRow("Monthly Installment:", self.monthly_installment)
        layout.addRow("Remaining Amount:", self.remaining_amount)
        layout.addRow("Add Payment:", self.payment_no)
        self.monthly_installment_previous=self.monthly_installment
        self.remaining_amount_previous=self.remaining_amount
        self.payment_no.textChanged.connect(self.calculate_installments)
        self.submit_button = QPushButton("Update Payment")
        layout.addWidget(self.submit_button)

    def calculate_installments(self):
        try:
            
            add_payment = float(self.payment_no.text() if self.payment_no.text() else 0)  # Added payment
            if not add_payment:  # If input is cleared, reset the remaining amount
                self.remaining_amount.setText(f"{self.remaining_amount_previous:.2f}")
                return
            months = int(self.duration.currentText())  # Get selected duration value
            remaining = float(self.remaining_amount.text() if self.remaining_amount.text() else 0)  # Get remaining amount

            updated_remaining = remaining - add_payment  # Subtract added payment

            monthly = updated_remaining / months if months else 0

            self.monthly_installment.setText(f"{monthly:.2f}")
            self.remaining_amount.setText(f"{updated_remaining:.2f}")

        except ValueError:
            # Clear fields if input is invalid
            self.monthly_installment.clear()
            self.remaining_amount.clear()
    
    # def calculate_installments(self):
    #     try:
    #         total_sale_price = float(self.sale_price.text())
    #         advance_payment = float(self.advance_cash.text() if self.advance_cash.text() else 0)
    #         months = int(self.duration.currentText())
    #         remaining = total_sale_price - advance_payment
    #         monthly = remaining / months if months else 0
    #         self.monthly_installment.setText(f"{monthly:.2f}")
    #         self.remaining_amount.setText(f"{remaining:.2f}")
    #     except ValueError:
    #         self.monthly_installment.clear()
    #         self.remaining_amount.clear()
    

    def submit_sale(self):
        # Implement the logic to submit the sale details to the database
        QMessageBox.information(self, "Submitted", "Sale details submitted successfully.")
        self.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = UserPage()
    window.show()
    app.exec()
