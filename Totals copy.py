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
import os,sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and frozen """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
class TotalsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Totals Amounts")
        self.setGeometry(200, 200, 800, 600)
        self.initUI()
        self.load_totals()

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


    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(10)

        # Logo
        logo_label = QLabel()
        logo_pixmap_path = resource_path('BM_moters.png')  # Use resource_path here
        logo_pixmap = QPixmap(logo_pixmap_path)
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
        headers = [
            "Total Purchase", "Purchase Price", "Total Sales", "Sales Price","Total Profit", "Total Expenses","Expense Amount","Profit\nAfter Expense", "Total\nRemaining Amount", "Total Cash"
        ]
        
        # Set the horizontal header labels
        table.setHorizontalHeaderLabels(headers)

        # Set tooltips for each header item
        for i in range(len(headers)):
            item = QTableWidgetItem(headers[i])
            # item.setToolTip(tooltips[i])  # Set tooltip for the column header
            table.setHorizontalHeaderItem(i, item)

        # Get the horizontal header
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
        self.load_expense(search_term)
        
        
    def load_totals(self):
        # Connect to database
        conn = sqlite3.connect("pos_database.db")  # Replace with your actual DB name
        cursor = conn.cursor()

        # Fetch totals
        cursor.execute("SELECT COUNT(*) FROM inventory")
        total_purchase = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(purchase_price), 0) FROM inventory")
        purchase_price = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM sales")
        total_sales = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(sale_price), 0) FROM sales")
        sales_price = cursor.fetchone()[0]

        total_profit = sales_price - purchase_price

        cursor.execute("SELECT COUNT(*) FROM expense")
        total_expenses = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(expense_price), 0) FROM expense")
        expense_amount = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(remaining_amount), 0) FROM sales")
        remaining_amount = cursor.fetchone()[0]
        
        Current_Profit = total_profit - expense_amount
        
        total_cash = Current_Profit - remaining_amount

        conn.close()  # Close connection

        # Convert values where needed (Expense Amount & Total Cash should be integers)
        purchase_price = int(purchase_price)
        sales_price = int(sales_price)
        total_profit = int(total_profit)
        expense_amount = int(expense_amount)
        Current_Profit = int(Current_Profit)
        remaining_amount = int(remaining_amount)
        total_cash = int(total_cash)

        # Populate the table
        self.table.setRowCount(1)
        
        # Function to create and center align table items
        def create_centered_item(value):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align text
            return item

        self.table.setItem(0, 0, create_centered_item(total_purchase))
        self.table.setItem(0, 1, create_centered_item(purchase_price))
        self.table.setItem(0, 2, create_centered_item(total_sales))
        self.table.setItem(0, 3, create_centered_item(sales_price))
        self.table.setItem(0, 4, create_centered_item(total_profit))
        self.table.setItem(0, 5, create_centered_item(total_expenses))
        self.table.setItem(0, 6, create_centered_item(expense_amount))
        self.table.setItem(0, 7, create_centered_item(Current_Profit))
        self.table.setItem(0, 8, create_centered_item(remaining_amount))
        self.table.setItem(0, 9, create_centered_item(total_cash))
    
        