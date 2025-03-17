import sqlite3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QHBoxLayout, QLabel, QLineEdit, QHeaderView, QApplication, QDialog, QFormLayout,QDateEdit, QCheckBox, QComboBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QFont

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

    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(14)  # Increase column count by one for the checkbox
        table.setHorizontalHeaderLabels([
            "Select", "Client Name", "Client CNIC", "Client Mobile No", "Bike Chassis No", "Sale Price", 
            "Purchase Date", "Sale Date", "Payment Method", "Duration", 
            "Advance Payment", "Monthly Installment", "Profit", "Status"
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


    def load_sales(self, search_term=""):
        self.connection = sqlite3.connect("pos_database.db")
        cursor = self.connection.cursor()
        query = """
            SELECT client_name, client_cnic, client_mobile, chassis_no, sale_price, 
                purchase_date, sale_date, payment_method, duration, advance_payment, 
                monthly_installment, profit, product_status 
            FROM sales
            WHERE client_name LIKE ? OR client_cnic LIKE ? OR client_mobile LIKE ? OR chassis_no LIKE ?
        """
        cursor.execute(query, ('%'+search_term+'%',)*4)
        records = cursor.fetchall()
        self.table.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            # Add a checkbox in the first column
            checkbox = QTableWidgetItem()
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row_idx, 0, checkbox)
            
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx + 1, QTableWidgetItem(str(col_data)))  # Adjust column index by +1
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

    def open_new_sale_dialog(self):
        dialog = NewSaleDialog(self)
        if dialog.exec():
            self.load_sales()

class NewSaleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Sale")
        self.setGeometry(300, 300, 400, 600)  # Adjusted for more fields
        layout = QFormLayout(self)

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
        self.installment_checkbox = QCheckBox("Installment")
        self.advance_cash = QLineEdit()
        self.duration = QComboBox()
        self.duration.addItems([str(i) for i in range(1, 13)])  # 1 to 12 months
        self.monthly_installment = QLineEdit()
        self.remaining_amount = QLineEdit()
        self.profit = QLineEdit()
        self.profit.setReadOnly(True)
        self.monthly_installment.setReadOnly(True)
        self.remaining_amount.setReadOnly(True)

        # Adding widgets to the layout
        layout.addRow("Client Name:", self.client_name)
        layout.addRow("Client Mobile Number:", self.client_mobile)
        layout.addRow("Client CNIC:", self.client_cnic)
        layout.addRow("Chassis No:", self.chassis_no)
        layout.addRow("Sale Price:", self.sale_price)
        layout.addRow("Sale Date:", self.sale_date)
        layout.addRow(self.installment_checkbox)
        layout.addRow("Advance Cash:", self.advance_cash)
        layout.addRow("Duration (Months):", self.duration)
        layout.addRow("Monthly Installment:", self.monthly_installment)
        layout.addRow("Remaining Amount:", self.remaining_amount)
        layout.addRow("Profit:", self.profit)

        self.submit_button = QPushButton("Submit Sale")
        self.submit_button.clicked.connect(self.submit_sale)
        layout.addWidget(self.submit_button)

        # Connect signals
        self.chassis_no.editingFinished.connect(self.fetch_purchase_price)
        self.sale_price.textChanged.connect(self.calculate_profit)
        self.installment_checkbox.toggled.connect(self.toggle_installment_fields)
        self.duration.currentIndexChanged.connect(self.calculate_installments)
        self.advance_cash.textChanged.connect(self.calculate_installments)

    def fetch_purchase_price(self):
        # Fetch purchase price from inventory based on chassis number
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT purchase_price FROM inventory WHERE chassis_no = ?", (self.chassis_no.text(),))
        result = cursor.fetchone()
        if result:
            self.purchase_price = result[0]
            self.calculate_profit()
        else:
            QMessageBox.warning(self, "Error", "Chassis number not found in inventory.")
        conn.close()

    def calculate_profit(self):
        try:
            sale_price = float(self.sale_price.text())
            profit = sale_price - self.purchase_price
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
        # Implement the logic to submit the sale details to the database
        QMessageBox.information(self, "Submitted", "Sale details submitted successfully.")
        self.accept()


if __name__ == "__main__":
    app = QApplication([])
    window = SalesPage()
    window.show()
    app.exec()
