import sqlite3
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QDialog, QLineEdit, QFormLayout, QHeaderView
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDateEdit
from PyQt6.QtCore import QDate

class InventoryPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(200, 200, 800, 600)
        self.purchase_price = QLineEdit(self)
        self.purchase_price.editingFinished.connect(self.check_purchase_price_validity)
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 lightgreen, stop:1 white);
            }
        """)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header_widget = self.create_header()
        main_layout.addWidget(header_widget)

        self.search_bar_layout = self.create_search_bar()
        main_layout.addLayout(self.search_bar_layout)

        self.table = self.setup_table()
        main_layout.addWidget(self.table)

        button_bar_layout = self.create_button_bar()
        main_layout.addLayout(button_bar_layout)

        self.load_inventory()

    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(10)

        logo_label = QLabel()
        logo_pixmap = QPixmap("BM_moters.png")
        if logo_pixmap.isNull():
            logo_pixmap = QPixmap(100, 60)
            logo_pixmap.fill(Qt.GlobalColor.gray)

        scaled_logo = logo_pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        header_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)

        header_text = QLabel("BISMILLAH MOTORS")
        header_text.setStyleSheet("color: white;")
        header_font = QFont("Arial", 24, QFont.Weight.Bold)
        header_text.setFont(header_font)
        header_layout.addStretch(1)
        header_layout.addWidget(header_text, 0, Qt.AlignmentFlag.AlignVCenter)
        header_layout.addStretch(1)

        return header_widget

    def create_button_bar(self):
        layout = QHBoxLayout()
        layout.addStretch(1)  # This will push the buttons to the right

        # Delete Inventory Button
        delete_button = self.create_styled_button("Delete Selected Inventory")
        delete_button.clicked.connect(self.delete_selected_inventory)
        layout.addWidget(delete_button)

        # Add Inventory Button
        add_button = self.create_styled_button("Add New Inventory")
        add_button.clicked.connect(self.open_add_inventory_dialog)
        layout.addWidget(add_button)

        layout.setContentsMargins(0, 0, 20, 20)  # Right padding to align with the data table margin

        return layout

    def create_styled_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #004d00;
                border: 2px solid #004d00;
                border-radius: 10px;
                padding: 5px;
                font-size: 13px;
                text-align: center;  /* Ensure text is centered */
            }
            QPushButton:hover {
                background-color: #c8ffc8;
            }
        """)
        button.setFixedSize(200, 30)  # Match dimensions with the search bar
        return button
    
    
    
    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(10)  
        table.setHorizontalHeaderLabels([
            "Select", "ID", "Bike Name", "Bike Model", "Chassis No", "Reg No", "Client Name",
            "Purchase Price","Purchase Date", "Status"
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
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)  # Correct way to disable selection

        return table


    
    def create_search_bar(self):
        layout = QHBoxLayout()
        layout.addStretch(1)  # Pushes the search bar to the right

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term here...")
        self.search_input.setFont(QFont("Arial", 10))  # Set font size programmatically
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
        self.search_input.textChanged.connect(self.on_search)
        layout.addWidget(self.search_input)
        layout.setContentsMargins(0, 0, 20, 0)

        return layout



    def on_search(self):
        search_term = self.search_input.text()
        self.load_inventory(search_term)
        
        
        
    def load_inventory(self, search_term=None):
        try:
            with sqlite3.connect("pos_database.db") as conn:
                cursor = conn.cursor()
                if search_term:
                    query = """
                        SELECT id, bike_name, bike_model, chassis_no, reg_no, client_name,purchase_price, purchase_date, product_status FROM inventory
                        WHERE bike_name LIKE ? OR bike_model LIKE ? OR chassis_no LIKE ? OR reg_no LIKE ? OR client_name LIKE ? OR purchase_date LIKE ? OR product_status LIKE ?
                    """
                    search_term = f'%{search_term}%'
                    cursor.execute(query, (search_term,) * 7)
                else:
                    query = """
                        SELECT id, bike_name, bike_model, chassis_no, reg_no, client_name,purchase_price, purchase_date, product_status, purchase_price FROM inventory
                    """
                    cursor.execute(query)

                records = cursor.fetchall()
                self.table.setRowCount(len(records))
                for index, row in enumerate(records):
                    # Set up the checkbox for selection
                    checkbox = QTableWidgetItem()
                    checkbox.setCheckState(Qt.CheckState.Unchecked)
                    self.table.setItem(index, 0, checkbox)
                    
                    # Populate other data
                    for col_index, data in enumerate(row, 1):
                        item = QTableWidgetItem(str(data))
                        item.setFlags(Qt.ItemFlag.ItemIsEnabled)  # Ensure the item is not editable
                        self.table.setItem(index, col_index, item)

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

    def check_purchase_price_validity(self):
        """ Checks if the purchase price input is valid and shows a warning if not. """
        if self.validate_purchase_price() is None:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the purchase price.")
            self.purchase_price.clear()

    def open_add_inventory_dialog(self):
        dialog = AddInventoryDialog()
        if dialog.exec():
            self.load_inventory()

    def delete_selected_inventory(self):
        selected_rows = [i for i in range(self.table.rowCount()) if self.table.item(i, 0).checkState() == Qt.CheckState.Checked]
        if not selected_rows:  # Corrected syntax here
            QMessageBox.warning(self, "No Selection", "No inventory selected for deletion.")
            return

        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        deleted_count = 0
        for row in selected_rows:
            inv_id = self.table.item(row, 1).text()
            cursor.execute("DELETE FROM inventory WHERE id = ?", (inv_id,))
            deleted_count += 1
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"Deleted {deleted_count} records successfully.")
        self.load_inventory()


class AddInventoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Inventory")
        self.setGeometry(300, 300, 400, 350)
        layout = QFormLayout(self)

        self.bike_name = QLineEdit()
        self.bike_model = QLineEdit()
        self.chassis_no = QLineEdit()
        self.reg_no = QLineEdit()
        self.client_name = QLineEdit()
        self.client_mobile = QLineEdit()
        self.client_cnic = QLineEdit()
        self.purchase_date = QDateEdit()
        self.purchase_date.setCalendarPopup(True)
        self.purchase_date.setDate(QDate.currentDate())
        self.purchase_date.setDisplayFormat("dd-MM-yyyy")
        self.purchase_price = QLineEdit()  # Field for entering purchase price

        layout.addRow("Bike Name:", self.bike_name)
        layout.addRow("Bike Model:", self.bike_model)
        layout.addRow("Chassis No (Unique):", self.chassis_no)
        layout.addRow("Reg No (Optional):", self.reg_no)
        layout.addRow("Client Name:", self.client_name)
        layout.addRow("Client Mobile:", self.client_mobile)
        layout.addRow("Client CNIC:", self.client_cnic)
        layout.addRow("Purchase Date", self.purchase_date)
        layout.addRow("Purchase Price:", self.purchase_price)  # Add purchase price to the form

        self.submit_button = QPushButton("Add Inventory")
        self.submit_button.clicked.connect(self.add_inventory)
        layout.addWidget(self.submit_button)

    def add_inventory(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        try:
            # Validate purchase price input
            try:
                purchase_price = float(self.purchase_price.text())
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the purchase price.")
                return  # Stop further processing if the input is invalid

            # Insert new inventory item, including validated purchase price
            cursor.execute(
                "INSERT INTO inventory (bike_name, bike_model, chassis_no, reg_no, client_name, client_mobile, client_cnic, purchase_date, purchase_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (self.bike_name.text(), self.bike_model.text(), self.chassis_no.text(), self.reg_no.text(), self.client_name.text(), self.client_mobile.text(), self.client_cnic.text(), self.purchase_date.date().toString("dd-MM-yyyy"), purchase_price)
            )
            sales_id_data = cursor.lastrowid 
            # Check if user already exists in the users table
            user_exists = cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM usersmanagement WHERE client_cnic = ?)",
                (self.client_cnic.text(),)
            ).fetchone()[0]
            if user_exists:
                cursor.execute(
                    "UPDATE usersmanagement SET inverted_id = ? WHERE client_cnic = ?",
                    (sales_id_data, self.client_cnic.text())
                )
            else:
                cursor.execute(
                    "INSERT INTO usersmanagement (client_name, client_mobile, client_cnic, date, inverted_id) VALUES (?, ?, ?, ?, ?)",
                    (self.client_name.text(), self.client_mobile.text(), self.client_cnic.text(), self.purchase_date.date().toString("yyyy-MM-dd"), sales_id_data)
                )
            # if not user_exists:
                # Insert new user if not exists
                # cursor.execute(
                #     "INSERT INTO usersmanagement (client_name, client_mobile, client_cnic, date,inverted_id) VALUES (?, ?, ?, ?, ?)",
                #     (self.client_name.text(), self.client_mobile.text(), self.client_cnic.text(), self.purchase_date.date().toString("yyyy-MM-dd"),sales_id_data)
                # )
                # cursor.execute(
                #     "INSERT INTO users (client_name, client_cnic, client_mobile, chassis_no, purchase_date) VALUES (?, ?, ?, ?, ?)",
                #     (self.client_name.text(), self.client_cnic.text(), self.client_mobile.text(), self.chassis_no.text(), self.purchase_date.date().toString("dd-MM-yyyy"))
                # )
            # else:
                # Update existing user data
                # cursor.execute(
                #     "INSERT INTO usersmanagement (client_name, client_mobile, client_cnic, date,sales_id) VALUES (?, ?, ?, ?, ?)",
                #     (self.client_name.text(), self.client_mobile.text(), self.client_cnic.text(), self.sale_date.date().toString("yyyy-MM-dd"),sales_id_data)
                # )
                # cursor.execute(
                #     "UPDATE users SET client_name = ?, client_mobile = ?, purchase_date = ? WHERE client_cnic = ?",
                #     (self.client_name.text(), self.client_mobile.text(), self.chassis_no.text(), self.purchase_date.date().toString("dd-MM-yyyy"), self.client_cnic.text())
                # )
            
            conn.commit()
            QMessageBox.information(self, "Success", "Inventory and User updated successfully!")
            self.accept()
            
        except sqlite3.IntegrityError as e:
            QMessageBox.warning(self, "Error", f"Failed to update due to an error: {str(e)}")
        finally:
            conn.close()

