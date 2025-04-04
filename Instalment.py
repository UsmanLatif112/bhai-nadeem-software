import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QLabel, QHBoxLayout, QHeaderView
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import os, sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and frozen """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Installment_pages(QWidget):
    def __init__(self, chassis_no, parent=None):
        super().__init__(parent)
        self.chassis_no = chassis_no
        self.setWindowTitle("Installment Management")
        self.setGeometry(200, 200, 900, 500)
        self.connection = sqlite3.connect("pos_database.db")
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        header_widget = self.create_header()
        self.layout.addWidget(header_widget)

        self.table = self.setup_table()
        self.layout.addWidget(self.table)

        self.load_payments()

    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")
        header_layout = QHBoxLayout(header_widget)

        # Logo
        logo_label = QLabel()
        logo_pixmap_path = resource_path('BM_moters.png')
        logo_pixmap = QPixmap(logo_pixmap_path)
        
        if logo_pixmap.isNull():
            print("Failed to load logo in header:", logo_pixmap_path)  # Debug output
            logo_pixmap = QPixmap(100, 60)  # Fallback size
            logo_pixmap.fill(Qt.GlobalColor.gray)
        
        scaled_logo = logo_pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        header_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)

        header_text = QLabel("BISMILLAH MOTORS")
        header_text.setStyleSheet("color: white;")
        header_text.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_layout.addStretch(1)
        header_layout.addWidget(header_text, 0, Qt.AlignmentFlag.AlignVCenter)
        header_layout.addStretch(1)

        return header_widget

    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        headers = ["Client Name", "Chassis No", "Payment", "Payment Date"]
        table.setHorizontalHeaderLabels(headers)
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
        return table

    def load_payments(self):
        cursor = self.connection.cursor()
        query = """
            SELECT client_name, chassis_no, payment_amount, payment_date
            FROM payments
            WHERE chassis_no = ? ORDER BY id DESC
        """
        cursor.execute(query, (self.chassis_no,))
        records = cursor.fetchall()
        self.table.setRowCount(len(records))
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.table.setItem(row_idx, col_idx, item)
        self.connection.close()

if __name__ == "__main__":
    app = QApplication([])
    # Example chassis number "ABC123" passed directly for testing
    window = Installment_pages("ABC123")
    window.show()
    app.exec()
