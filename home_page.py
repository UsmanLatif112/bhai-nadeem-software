from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from inventory import InventoryPage
from sales import SalesPage
from user_maagement import UserManagement

class HomePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bismillah Motors - Home")
        self.setGeometry(100, 100, 800, 600)  # Starting window size
        
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Gradient background
        central_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1: 0, y1: 0, 
                    x2: 1, y2: 1,
                    stop: 0  lightgreen, 
                    stop: 1  white
                );
            }
        """)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Header section
        header_widget = QWidget()
        header_widget.setFixedHeight(80)  # You can adjust this height
        header_widget.setStyleSheet("background-color: #004d00;")

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(10)

        # Logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("BM_moters.png")
        if logo_pixmap.isNull():
            logo_pixmap = QPixmap(100, 60)
            logo_pixmap.fill(Qt.GlobalColor.gray)

        scaled_logo = logo_pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(scaled_logo)
        header_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)

        # Header text
        header_text = QLabel("BISMILLAH MOTORS")
        header_text.setStyleSheet("color: white;")
        header_font = QFont("Arial", 24, QFont.Weight.Bold)
        header_text.setFont(header_font)

        # Stretch to balance layout around the text
        header_layout.addStretch(1)
        header_layout.addWidget(header_text, 0, Qt.AlignmentFlag.AlignVCenter)
        header_layout.addStretch(1)

        main_layout.addWidget(header_widget)

        # Button section
        button_layout = QVBoxLayout()
        button_layout.addStretch(1)  # Center buttons vertically

        def create_button(text):
            button = QPushButton(text)
            button.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: #004d00;
                    border: 2px solid #004d00;
                    border-radius: 15px;
                    padding: 10px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #c8ffc8;
                }
            """)
            button.setFixedSize(220, 50)  # Adjust button size as needed
            return button

        inventory_button = create_button("Inventory Management")
        inventory_button.clicked.connect(self.open_inventory_page)
        button_layout.addWidget(inventory_button, 0, Qt.AlignmentFlag.AlignHCenter)

        sales_button = create_button("Sales Management")
        sales_button.clicked.connect(self.open_sales_page)
        button_layout.addWidget(sales_button, 0, Qt.AlignmentFlag.AlignHCenter)

        users_button = create_button("User Management")
        users_button.clicked.connect(self.open_user_management_page)
        button_layout.addWidget(users_button, 0, Qt.AlignmentFlag.AlignHCenter)

        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)

    def open_inventory_page(self):
        self.inventory_page = InventoryPage()
        self.inventory_page.show()

    def open_sales_page(self):
        self.sales_page = SalesPage()
        self.sales_page.show()

    def open_user_management_page(self):
        self.user_management_page = UserManagement()
        self.user_management_page.show()
