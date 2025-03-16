# users.py
import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox

class UserManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(200, 200, 700, 400)
        self.layout = QVBoxLayout(self)
        self.init_ui()
        self.load_users()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Client Name", "CNIC", "Mobile No", "Inventory ID", "Status", "Purchase Date", "Sale Date", "Payment Method"])
        self.layout.addWidget(self.table)

        self.delete_button = QPushButton("Delete Selected User")
        self.delete_button.clicked.connect(self.delete_selected_user)
        self.layout.addWidget(self.delete_button)

    def load_users(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT client_name, client_cnic, client_mobile, inventory_id, product_status, purchase_date, sale_date, payment_method FROM users")
        records = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def delete_selected_user(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            inventory_id = self.table.item(selected_row, 3).text()  # Assuming 'inventory_id' is in column index 3
            self.delete_user(inventory_id)

    def delete_user(self, inventory_id):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE inventory_id = ?", (inventory_id,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "User deleted successfully!")
        self.load_users()
