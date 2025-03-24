import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt

class UserDetail(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.connection = sqlite3.connect("pos_database.db")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Details")
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout(self)
        
        # Fetch user details
        self.user_details = self.fetch_user_details()
        
        # Display user details
        self.name_label = QLabel(f"Name: {self.user_details['client_name']}")
        self.mobile_label = QLabel(f"Mobile: {self.user_details['client_mobile']}")
        self.cnic_label = QLabel(f"CNIC: {self.user_details['client_cnic']}")
        self.date_label = QLabel(f"Date: {self.user_details['date']}")
        
        layout.addWidget(self.name_label)
        layout.addWidget(self.mobile_label)
        layout.addWidget(self.cnic_label)
        layout.addWidget(self.date_label)
        
        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

    def fetch_user_details(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT client_name, client_mobile, client_cnic, date
            FROM usersmanagement
            WHERE id = ?
        """, (self.user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "client_name": row[0],
                "client_mobile": row[1],
                "client_cnic": row[2],
                "date": row[3]
            }
        else:
            QMessageBox.warning(self, "Error", "No user found with the provided ID.")
            return {}

    def closeEvent(self, event):
        self.connection.close()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Example user ID, replace with actual user ID as needed
    detail_window = UserDetail(user_id=1)
    detail_window.show()
    sys.exit(app.exec())
