import sqlite3
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QDialog, QLineEdit, QFormLayout, QHeaderView, QComboBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDateEdit

from PyQt6.QtCore import QDate, Qt
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
        table.setColumnCount(13)  # Updated to 13 columns
        headers = [
            "Total\nPurchase Count",
            "Total\nPurchase Price",
            "Total\nInventory",          # New column
            "Inventory\nPurchasing",     # New column
            "Total\nSales Count",
            "Total Sales\nSum",
            "Total Profit",
            "Total\nExpenses Count",
            "Total\nExpenses Sum",
            "Profit\nAfter Expense",
            "Total\nRemaining Amount",
            "Cash\nIn Hand",
            "Total Cash\nAfter Remaining"
        ]
        # The tooltips for the new columns
        tooltips = [
            "Number of purchases (inventory items bought) in this period",
            "Sum of all purchase prices",
            "Total count of items in inventory with status 'purchased'",  # Tooltip for new column
            "Sum of purchase prices of items in inventory with status 'purchased'",  # Tooltip for new column
            "Number of sales in this period",
            "Sum of all sales prices",
            "Total profit (sales sum minus purchase prices)",
            "Number of expenses recorded in this period",
            "Sum of all expenses in this period",
            "Profit after deducting expenses from profit",
            "Sum of amounts still to be received from sales",
            "Cash in hand (total sales sum - expenses)",
            "Total sales after subtracting remaining amount (cash in hand - remaining)"
        ]
        table.setHorizontalHeaderLabels(headers)
        for i, (header, tip) in enumerate(zip(headers, tooltips)):
            item = QTableWidgetItem(header)
            item.setToolTip(tip)
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
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        return table



    
    def create_search_bar(self):
        layout = QHBoxLayout()
        layout.addStretch(1)  # Push search bar to the right

        # Filter Dropdown
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(["Today", "7 Days", "1 Month", "3 Months", "6 Months", "12 Months", "Custom"])
        self.filter_dropdown.setFixedHeight(30)
        self.filter_dropdown.setFixedWidth(120)
        self.filter_dropdown.currentIndexChanged.connect(self.on_filter_change)
        layout.addWidget(self.filter_dropdown)

        # Date Picker for Start Date
        self.date_picker_start = QDateEdit()
        self.date_picker_start.setCalendarPopup(True)
        self.date_picker_start.setDate(QDate.currentDate())
        self.date_picker_start.setDisplayFormat("yyyy-MM-dd")
        self.date_picker_start.setFixedHeight(30)
        self.date_picker_start.setFixedWidth(120)
        self.date_picker_start.setEnabled(False)
        # Initially disabled, enabled when 'Custom' is selected in the dropdown
        self.date_picker_start.setStyleSheet("""
            QDateEdit {
                background-color: white;
                color: #004d00;
                border: 2px solid #004d00;
                padding: 5px 10px;
            }
            QDateEdit QCalendarWidget {
                background-color: white;
                color: black;
            }
            QCalendarWidget QToolButton {
                color: black;
                background-color: white;
                border: none;
            }
            QCalendarWidget QSpinBox {
                color: black;
                background-color: white;
                border: 2px solid #004d00;
            }
            QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: right;
            }
            QCalendarWidget QSpinBox::up-arrow, QCalendarWidget QSpinBox::down-arrow {
                width: 15px;
                height: 15px;
            }
            QCalendarWidget QMenu {
                background-color: white;
                border: 1px solid #004d00;
            }
            QCalendarWidget QWidget {
                color: black;
            }
            QCalendarWidget QTableView {
                background-color: white;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #004d00;
                color: white;
            }
        """)
        layout.addWidget(self.date_picker_start)

        # Date Picker for End Date
        self.date_picker_end = QDateEdit()
        self.date_picker_end.setCalendarPopup(True)
        self.date_picker_end.setDate(QDate.currentDate())
        self.date_picker_end.setDisplayFormat("yyyy-MM-dd")
        self.date_picker_end.setFixedHeight(30)
        self.date_picker_end.setFixedWidth(120)
        self.date_picker_end.setEnabled(False)
        # Initially disabled, enabled when 'Custom' is selected in the dropdown
        self.date_picker_end.setStyleSheet("""
            QDateEdit {
                background-color: white;
                color: #004d00;
                border: 2px solid #004d00;
                padding: 5px 10px;
            }
            QDateEdit QCalendarWidget {
                background-color: white;
                color: black;
            }
            QCalendarWidget QToolButton {
                color: black;
                background-color: white;
                border: none;
            }
            QCalendarWidget QSpinBox {
                color: black;
                background-color: white;
                border: 2px solid #004d00;
            }
            QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {
                subcontrol-origin: border;
                subcontrol-position: right;
            }
            QCalendarWidget QSpinBox::up-arrow, QCalendarWidget QSpinBox::down-arrow {
                width: 15px;
                height: 15px;
            }
            QCalendarWidget QMenu {
                background-color: white;
                border: 1px solid #004d00;
            }
            QCalendarWidget QWidget {
                color: black;
            }
            QCalendarWidget QTableView {
                background-color: white;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #004d00;
                color: white;
            }
        """)
        layout.addWidget(self.date_picker_end)
        

        # Apply Button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setFixedHeight(30)
        self.apply_button.setFixedWidth(80)
        self.apply_button.setStyleSheet("background-color: #004d00; color: white; border-radius: 5px;")
        self.apply_button.clicked.connect(self.load_totals)
        layout.addWidget(self.apply_button)

        layout.setContentsMargins(0, 0, 20, 0)
        return layout
        
    def on_filter_change(self):
        if self.filter_dropdown.currentText() == "Custom":
            self.date_picker_start.setEnabled(True)
            self.date_picker_end.setEnabled(True)
        else:
            self.date_picker_start.setEnabled(False)
            self.date_picker_end.setEnabled(False)
            
            
    def load_totals(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()

        selected_filter = self.filter_dropdown.currentText()
        today = QDate.currentDate().toString("yyyy-MM-dd")

        if selected_filter == "Today":
            sales_condition = f"DATE(sale_date) = '{today}'"
            inventory_condition = f"DATE(purchase_date) = '{today}'"
            expense_condition = f"DATE(expense_date) = '{today}'"
            inventory_filter_condition = f"DATE(purchase_date) = '{today}'"  # For inventory filtering
        elif selected_filter == "7 Days":
            sales_condition = f"DATE(sale_date) >= DATE('{today}', '-7 days')"
            inventory_condition = f"DATE(purchase_date) >= DATE('{today}', '-7 days')"
            expense_condition = f"DATE(expense_date) >= DATE('{today}', '-7 days')"
            inventory_filter_condition = f"DATE(purchase_date) >= DATE('{today}', '-7 days')"  # For inventory filtering
        elif selected_filter == "1 Month":
            start_date = QDate.currentDate().addMonths(-1).toString("yyyy-MM-dd")
            sales_condition = f"DATE(sale_date) BETWEEN '{start_date}' AND '{today}'"
            inventory_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{today}'"
            expense_condition = f"DATE(expense_date) BETWEEN '{start_date}' AND '{today}'"
            inventory_filter_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{today}'"  # For inventory filtering
        elif selected_filter == "3 Months":
            start_date = QDate.currentDate().addMonths(-3).toString("yyyy-MM-dd")
            sales_condition = f"DATE(sale_date) BETWEEN '{start_date}' AND '{today}'"
            inventory_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{today}'"
            expense_condition = f"DATE(expense_date) BETWEEN '{start_date}' AND '{today}'"
            inventory_filter_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{today}'"  # For inventory filtering
        elif selected_filter == "6 Months":
            start_date = QDate.currentDate().addMonths(-6).toString("yyyy-MM-dd")
            sales_condition = f"DATE(sale_date) BETWEEN '{start_date}' AND '{today}'"
            inventory_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{today}'"
            expense_condition = f"DATE(expense_date) BETWEEN '{start_date}' AND '{today}'"
            inventory_filter_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{today}'"  # For inventory filtering
        elif selected_filter == "12 Months":
            start_date = QDate.currentDate().addMonths(-12).toString("yyyy-MM-dd")
            sales_condition = f"DATE(sale_date) BETWEEN '{start_date}' AND '{today}'"
            inventory_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{today}'"
            expense_condition = f"DATE(expense_date) BETWEEN '{start_date}' AND '{today}'"
            inventory_filter_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{today}'"  # For inventory filtering
        elif selected_filter == "Custom":
            start_date = self.date_picker_start.date().toString("yyyy-MM-dd")
            end_date = self.date_picker_end.date().toString("yyyy-MM-dd")
            sales_condition = f"DATE(sale_date) BETWEEN '{start_date}' AND '{end_date}'"
            inventory_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{end_date}'"
            expense_condition = f"DATE(expense_date) BETWEEN '{start_date}' AND '{end_date}'"
            inventory_filter_condition = f"DATE(purchase_date) BETWEEN '{start_date}' AND '{end_date}'"  # For inventory filtering
        else:
            sales_condition = "1=1"
            inventory_condition = "1=1"
            expense_condition = "1=1"
            inventory_filter_condition = "1=1"

        # Purchases
        cursor.execute(f"SELECT COUNT(*), COALESCE(SUM(purchase_price), 0) FROM inventory WHERE {inventory_condition}")
        total_purchase_count, total_purchase_price = cursor.fetchone()

        # New Queries for Total Inventory and Inventory Purchasing
        cursor.execute(f"""
            SELECT COUNT(*), COALESCE(SUM(purchase_price), 0)
            FROM inventory
            WHERE product_status = 'Purchased' AND {inventory_filter_condition}
        """)
        total_inventory_count, inventory_purchasing_sum = cursor.fetchone()

        # Sales
        cursor.execute(f"""
            SELECT
                COUNT(*),                        
                COALESCE(SUM(sale_price), 0),    
                COALESCE(SUM(remaining_amount), 0) 
            FROM sales
            WHERE {sales_condition}
        """)
        total_sales_count, total_sales_sum, total_remaining_amount = cursor.fetchone()

        # Total profit from sales table
        cursor.execute(f"SELECT COALESCE(SUM(profit), 0) FROM sales WHERE {sales_condition}")
        total_profit = cursor.fetchone()[0]

        # Expenses
        cursor.execute(f"SELECT COUNT(*), COALESCE(SUM(expense_price), 0) FROM expense WHERE {expense_condition}")
        total_expenses_count, total_expenses_sum = cursor.fetchone()

        # Cash in Hand
        cash_in_hand = total_sales_sum - total_expenses_sum
        total_sales_after_remaining = cash_in_hand - total_remaining_amount
        profit_after_expense = total_profit - total_expenses_sum

        values = [
            int(total_purchase_count),            # Total Purchase Count
            int(total_purchase_price),            # Total Purchase Price
            int(total_inventory_count),           # Total Inventory Count (Purchased)
            int(inventory_purchasing_sum),       # Inventory Purchasing (Sum of Purchase Prices)
            int(total_sales_count),               # Total Sales Count
            int(total_sales_sum),                 # Total Sales Sum
            int(total_profit),                    # Total Profit from Sales
            int(total_expenses_count),            # Total Expenses Count
            int(total_expenses_sum),              # Total Expenses Sum
            int(profit_after_expense),            # Profit After Expense
            int(total_remaining_amount),          # Total Remaining Amount
            int(cash_in_hand),                    # Cash In Hand
            int(total_sales_after_remaining)      # Total Sales After Remaining Amount
        ]

        cell_tooltips = [
            "Number of purchases = ",
            "Sum of Purchase prices = ",
            "Total inventory count (purchased) = ",  # Tooltip for new column
            "Sum of inventory purchases (purchased) = ",  # Tooltip for new column
            "Number of sales = ",
            "Sum of all sales prices = ",
            "Total profit (from sales table) = ",
            "Number of expenses = ",
            "Sum of all expenses = ",
            "Profit after deducting expenses = ",
            "Sum of Remaining amounts = ",
            "Cash in hand (total sales sum - expenses) = ",
            "Total sales after subtracting remaining (cash in hand - remaining) = "
        ]

        self.table.setRowCount(1)
        for col, (value, tip) in enumerate(zip(values, cell_tooltips)):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setToolTip(f"{tip}{value}")
            self.table.setItem(0, col, item)

        conn.close()
