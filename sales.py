# sales.py
import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox

class SalesPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Management")
        self.setGeometry(200, 200, 900, 500)
        self.layout = QVBoxLayout(self)
        self.init_ui()
        self.load_sales()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels(["Client Name", "CNIC", "Mobile No", "Bike Reg No", "Sale Price", "Purchase Date", "Sale Date", "Payment Method", "Duration", "Advance Payment", "Monthly Installment", "Profit", "Status"])
        self.layout.addWidget(self.table)

        self.add_sale_button = QPushButton("Add New Sale")
        self.add_sale_button.clicked.connect(self.open_new_sale_dialog)
        self.layout.addWidget(self.add_sale_button)

        self.delete_button = QPushButton("Delete Selected Sale")
        self.delete_button.clicked.connect(self.delete_selected_sale)
        self.layout.addWidget(self.delete_button)

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

    def delete_selected_sale(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            reg_no = self.table.item(selected_row, 3).text()
            self.delete_sale(reg_no)

    def delete_sale(self, reg_no):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales WHERE reg_no = ?", (reg_no,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Sale record deleted successfully!")
        self.load_sales()

    def open_new_sale_dialog(self):
        # This method should open a dialog to create a new sale.
        pass
