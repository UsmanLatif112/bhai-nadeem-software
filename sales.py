import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QHBoxLayout, QLabel, QLineEdit, QHeaderView, QApplication, QDialog, QFormLayout,QDateEdit, QCheckBox, QComboBox
)
from PyQt6.QtGui import QPixmap, QFont, QTextOption
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QFont

from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtCore import QSize


from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtCore import Qt, QSize, QRectF
from PyQt6.QtGui import QTextOption

class HeaderDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()
        
        # Set up text option for word wrapping
        text_option = QTextOption()
        text_option.setWrapMode(QTextOption.WrapMode.WordWrap)
        
        # Draw the header item with wrapped text
        painter.drawText(QRectF(option.rect), index.data(), text_option)
        painter.restore()

    def sizeHint(self, option, index):
        return QSize(100, 40)  # Customize size for headers


class SalesPage(QWidget):
    def __init__(self):
        super().__init__()
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

        self.add_sale_button = QPushButton("Add New Sale")
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
    
    # def setup_table(self):
    #     table = QTableWidget()
    #     table.setColumnCount(15)
    #     table.setHorizontalHeaderLabels([
    #         "Select", "Client\nName", "Client\nCNIC", "Client Mobile\nNo", "Chassis No", 
    #         "Sale\nPrice", "Purchase\nPrice", "Sale\nDate", "Profit", "Payment\nMethod",
    #         "Remaining\nAmount", "Duration", "Advance\nPayment", "Monthly\nInstallment", "Status"
    #     ])
        
    #     # Set tooltips for headers
    #     header_labels = [
    #         "Select", "Client\nName", "Client\nCNIC", "Client Mobile\nNo", "Chassis No", 
    #         "Sale\nPrice", "Purchase\nPrice", "Sale\nDate", "Profit", "Payment\nMethod",
    #         "Remaining\nAmount", "Duration", "Advance\nPayment", "Monthly\nInstallment", "Status"
    #     ]
        
    #     for i, label in enumerate(header_labels):
    #         item = table.horizontalHeaderItem(i)
    #         if item is not None:
    #             item.setToolTip(label)

    #     header = table.horizontalHeader()
    #     header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

    #     # Set specific widths for columns to avoid bottom scrollbar
    #     column_widths = [50, 120, 100, 100, 100, 100, 100, 100, 100, 120, 120, 80, 120, 120, 100]
    #     for i, width in enumerate(column_widths):
    #         header.resizeSection(i, width)

    #     # Set the item delegate for the header
    #     table.setItemDelegateForColumn(0, HeaderDelegate())

    #     table.setStyleSheet("""
    #         QTableWidget {
    #             background-color: white;
    #             gridline-color: #004d00;
    #             font-size: 14px;
    #             color: black;
    #             margin: 10px;
    #         } 
    #         QHeaderView::section {
    #             background-color: #004d00;
    #             color: white;
    #             font-weight: bold;
    #             padding: 5px;  /* Padding for better visual appearance */
    #         }
    #     """)
        
    #     table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
    #     table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        
    #     return table

    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(15)
        
        headers = [
            "Select", "Client\nName", "Client\nCNIC", "Client\nMobileNo", "Chassis\nNo", 
            "Sale\nPrice", "Purchase\nPrice", "Sale\nDate", "Profit", "Payment\nMethod",
            "Remaining\nAmount", "Duration", "Advance\nPayment", "Monthly\nInstallment", "Status"
        ]
        
        tooltips = [
            "Select", "Client Name", "Client CNIC", "Client MobileNo", "Chassis No", 
            "Sale Price", "Purchase Price", "Sale Date", "Profit", "Payment Method",
            "Remaining Amount", "Duration", "Advance Payment", "Monthly Installment", "Status"
        ]

        # Set horizontal header labels
        table.setHorizontalHeaderLabels(headers)

        # Set tooltips for each header item
        for i in range(len(headers)):
            item = QTableWidgetItem(headers[i])
            item.setToolTip(tooltips[i])  # Setting tooltip on the header item
            table.setHorizontalHeaderItem(i, item)

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
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)  # Correct value to disable selection
        
        return table




    # def load_sales(self, search_term=""):
    #     self.connection = sqlite3.connect("pos_database.db")
    #     cursor = self.connection.cursor()
    #     query = """
    #         SELECT client_name, client_cnic, client_mobile, chassis_no, sale_price, 
    #             purchase_price, sale_date, profit, payment_method, remaining_amount, 
    #             duration, advance_payment, monthly_installment, product_status 
    #         FROM sales
    #         WHERE client_name LIKE ? OR client_cnic LIKE ? OR client_mobile LIKE ? OR chassis_no LIKE ?
    #     """
    #     cursor.execute(query, ('%'+search_term+'%',)*4)
    #     records = cursor.fetchall()
    #     self.table.setRowCount(len(records))
    #     for row_idx, row_data in enumerate(records):
    #         checkbox = QTableWidgetItem()
    #         checkbox.setCheckState(Qt.CheckState.Unchecked)
    #         self.table.setItem(row_idx, 0, checkbox)
    #         for col_idx, col_data in enumerate(row_data):
    #             self.table.setItem(row_idx, col_idx + 1, QTableWidgetItem(str(col_data)))
    #     self.connection.close()

    def load_sales(self, search_term=""):
        self.connection = sqlite3.connect("pos_database.db")
        cursor = self.connection.cursor()
        query = """
            SELECT client_name, client_cnic, client_mobile, chassis_no, sale_price, 
                purchase_price, sale_date, profit, payment_method, remaining_amount, 
                duration, advance_payment, monthly_installment, product_status 
            FROM sales 
            WHERE client_name LIKE ? OR client_cnic LIKE ? OR client_mobile LIKE ? OR chassis_no LIKE ? ORDER BY id DESC
        """
        cursor.execute(query, ('%'+search_term+'%',)*4)
        records = cursor.fetchall()
        self.table.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            checkbox = QTableWidgetItem()
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row_idx, 0, checkbox)  # Add checkboxes to the first column

            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_idx, col_idx + 1, item)  # Fill other data
        self.connection.close()


    def delete_selected_sale(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        try:
            needs_refresh = False
            for row in range(self.table.rowCount()):
                checkbox_item = self.table.item(row, 0)  # Index 0 for checkbox column
                if checkbox_item.checkState() == Qt.CheckState.Checked:
                    chassis_no = self.table.item(row, 4).text()  # Assuming chassis_no is in column 4
                    cursor.execute("DELETE FROM sales WHERE chassis_no = ?", (chassis_no,))
                    cursor.execute(
                        "UPDATE inventory SET product_status = 'Purchased' WHERE chassis_no = ?",
                        (chassis_no,)
                        )
                    needs_refresh = True

            if needs_refresh:
                conn.commit()
                QMessageBox.information(self, "Success", "Selected sales records deleted successfully!")
                # Update or insert user data
                self.load_sales()  # Refresh the table
            else:
                QMessageBox.warning(self, "No Selection", "Please select at least one sale to delete.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"An error occurred while trying to delete the sale: {str(e)}")
        finally:
            conn.close()

    def delete_sale(self, chassis_no):
        reply = QMessageBox.question(self, 'Confirm Deletion', "Are you sure you want to delete this sale?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = sqlite3.connect("pos_database.db")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM sales WHERE chassis_no = ?", (chassis_no,))
                conn.commit()
                QMessageBox.information(self, "Success", "Sale record deleted successfully!")
                self.load_sales()  # Refresh the table to show that the record has been deleted
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Error", f"An error occurred while trying to delete the sale: {str(e)}")
            finally:
                conn.close()
        else:
            QMessageBox.information(self, "Cancelled", "Sale deletion cancelled.")


    def open_new_sale_dialog(self):
        dialog = NewSaleDialog(self)
        if dialog.exec():
            self.load_sales()
    
class NewSaleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Sale")
        self.setGeometry(300, 300, 400, 600)
        layout = QFormLayout(self)
        # self.setup_ui()
        self.connection = sqlite3.connect("pos_database.db")

        # Input fields
        self.client_name = QLineEdit()
        self.client_mobile = QLineEdit()
        self.client_cnic = QLineEdit()
        self.chassis_no = QLineEdit()
        self.sale_price = QLineEdit()
        self.sale_date = QDateEdit()
        self.sale_date.setCalendarPopup(True)
        self.sale_date.setDate(QDate.currentDate())
        self.sale_date.setDisplayFormat("dd-MM-yyyy")
        self.purchase_price = QLineEdit()
        self.purchase_price.setReadOnly(True)  # Purchase price is not editable
        self.profit = QLineEdit()
        self.profit.setReadOnly(True)
        self.installment_checkbox = QCheckBox("Installment")
        self.installment_checkbox.setChecked(False)  # Start unchecked
        self.advance_cash = QLineEdit()
        self.advance_cash.setEnabled(False)
        self.duration = QComboBox()
        self.duration.addItems([str(i) for i in range(1, 13)])  # 1 to 12 months
        self.duration.setEnabled(False)
        self.monthly_installment = QLineEdit()
        self.monthly_installment.setReadOnly(True)
        self.monthly_installment.setEnabled(False)
        self.remaining_amount = QLineEdit()
        self.remaining_amount.setReadOnly(True)
        self.remaining_amount.setEnabled(False)

        # Adding widgets to the layout
        layout.addRow("Client Name:", self.client_name)
        layout.addRow("Client Mobile Number:", self.client_mobile)
        layout.addRow("Client CNIC:", self.client_cnic)
        layout.addRow("Chassis No:", self.chassis_no)
        layout.addRow("Purchase Price:", self.purchase_price)
        layout.addRow("Sale Price:", self.sale_price)
        layout.addRow("Profit:", self.profit)
        layout.addRow("Sale Date:", self.sale_date)
        layout.addRow(self.installment_checkbox)
        layout.addRow("Advance Cash:", self.advance_cash)
        layout.addRow("Duration (Months):", self.duration)
        layout.addRow("Monthly Installment:", self.monthly_installment)
        layout.addRow("Remaining Amount:", self.remaining_amount)

        self.submit_button = QPushButton("Submit Sale")
        self.submit_button.clicked.connect(self.submit_sale)
        layout.addWidget(self.submit_button)

        # Connect signals
        self.chassis_no.editingFinished.connect(self.fetch_purchase_price)
        self.sale_price.textChanged.connect(self.calculate_profit)
        self.installment_checkbox.toggled.connect(self.toggle_installment_fields)
        self.advance_cash.textChanged.connect(self.calculate_installments)
        self.duration.currentIndexChanged.connect(self.calculate_installments)
    def fetch_purchase_price(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()

        try:
            # Execute the query to get purchase price and product status
            cursor.execute("SELECT purchase_price, product_status FROM inventory WHERE chassis_no = ?", (self.chassis_no.text(),))
            result = cursor.fetchone()

            if result:
                purchase_price, product_status = result  # Unpack results directly

                # Check if the product status is 'Sold'
                if product_status == 'Sold':
                    QMessageBox.warning(self, "Error", "This chassis number is already sold.")
                    self.purchase_price.clear()
                else:
                    # Set the purchase price and calculate profit if not sold
                    self.purchase_price.setText(str(purchase_price))
                    self.calculate_profit()
            else:
                # No record found with the given chassis number
                QMessageBox.warning(self, "Error", "Chassis number not found in inventory.")
                self.purchase_price.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

    def calculate_profit(self):
        try:
            sale_price = float(self.sale_price.text())
            purchase_price = float(self.purchase_price.text())
            profit = sale_price - purchase_price
            self.profit.setText(str(profit))
        except ValueError:
            self.profit.clear()

    def toggle_installment_fields(self, checked):
        self.advance_cash.setEnabled(checked)
        self.duration.setEnabled(checked)
        self.monthly_installment.setEnabled(checked)
        self.remaining_amount.setEnabled(checked)
        if not checked:
            self.advance_cash.clear()
            self.duration.setCurrentIndex(0)
            self.monthly_installment.clear()
            self.remaining_amount.clear()

    def calculate_installments(self):
        try:
            total_sale_price = float(self.sale_price.text())
            advance_payment = float(self.advance_cash.text() if self.advance_cash.text() else 0)
            months = int(self.duration.currentText())
            remaining = total_sale_price - advance_payment
            monthly = remaining / months if months else 0
            self.monthly_installment.setText(f"{monthly:.2f}")
            self.remaining_amount.setText(f"{remaining:.2f}")
        except ValueError:
            self.monthly_installment.clear()
            self.remaining_amount.clear()

    def submit_sale(self):
        try:
            sale_price = float(self.sale_price.text()) if self.sale_price.text() else 0
            advance_payment = float(self.advance_cash.text()) if self.advance_cash.text() else 0
            monthly_installment = float(self.monthly_installment.text()) if self.monthly_installment.text() else 0
            profit = float(self.profit.text()) if self.profit.text() else 0
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please ensure all prices are valid numbers.")
            return

        payment_method = "On Installment" if self.installment_checkbox.isChecked() else "Net Cash"
        remaining_amount = 0
        if self.installment_checkbox.isChecked():
            total_sale_price = sale_price
            months = int(self.duration.currentText())
            remaining_amount = total_sale_price - advance_payment
            if months > 0:
                monthly_installment = remaining_amount / months

        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO sales (client_name, client_cnic, client_mobile, chassis_no, sale_price, sale_date, payment_method, duration, purchase_price, advance_payment, monthly_installment, profit, remaining_amount, product_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Sold')",
                (
                    self.client_name.text(),
                    self.client_cnic.text(),
                    self.client_mobile.text(),
                    self.chassis_no.text(),
                    sale_price,
                    self.sale_date.date().toString("yyyy-MM-dd"),  # Convert PyQt date to string
                    payment_method,
                    int(self.duration.currentText()) if self.installment_checkbox.isChecked() else 0,
                    float(self.purchase_price.text()) if self.purchase_price.text() else 0,  # Ensure correct data type
                    advance_payment,
                    monthly_installment,
                    profit,
                    remaining_amount,
                )
                )
            sales_id_data = cursor.lastrowid 
            cursor.execute(
                "UPDATE inventory SET product_status = 'Sold' WHERE chassis_no = ?",
                (self.chassis_no.text(),)
                )
                # Update or insert user data
            user_exists = cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM usersmanagement WHERE client_cnic = ?)",
                (self.client_cnic.text(),)
            ).fetchone()[0]
            if user_exists: 
                cursor.execute(
                    "UPDATE usersmanagement SET sales_id = ? WHERE client_cnic = ?",
                    (sales_id_data, self.client_cnic.text())
                )
            else:
                cursor.execute(
                    "INSERT INTO usersmanagement (client_name, client_mobile, client_cnic, date, sales_id) VALUES (?, ?, ?, ?, ?)",
                    (self.client_name.text(), self.client_mobile.text(), self.client_cnic.text(), self.sale_date.date().toString("yyyy-MM-dd"), sales_id_data)
                )
            # if not user_exists:
            #     cursor.execute(
            #             "INSERT INTO usersmanagement (client_name, client_mobile, client_cnic, date,sales_id) VALUES (?, ?, ?, ?, ?)",
            #             (self.client_name.text(), self.client_mobile.text(), self.client_cnic.text(), self.sale_date.date().toString("yyyy-MM-dd"),sales_id_data)
            #         )
                
            self.connection.commit()
            QMessageBox.information(self, "Success", "Sale added successfully.")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
        finally:
            self.connection.close()
            self.accept()
            if self.parent():
                self.parent().load_sales()  # Refresh the sales table

        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = SalesPage()
    window.show()
    app.exec()
