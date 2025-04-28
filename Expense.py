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
    
class ExpensePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Expense Management")
        self.setGeometry(200, 200, 800, 600)
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

        self.load_expense()

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

        # Delete Inventory Button
        delete_button = self.create_styled_button("Delete Selected Expense")
        delete_button.clicked.connect(self.delete_selected_expense)
        layout.addWidget(delete_button)

        # Add Inventory Button
        add_button = self.create_styled_button("Add New Expense")
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
        table.setColumnCount(5)
        headers = [
            "Select", "Expense", "Description", "Expense Price", "Expense Date"
        ]
        tooltips = [
            "Check to select this expense", 
            "Expense name/type",
            "Description/details of the expense",
            "The price/amount of this expense",
            "Date when the expense was made"
        ]
        
        # Set the horizontal header labels and tooltips
        for i in range(len(headers)):
            item = QTableWidgetItem(headers[i])
            item.setToolTip(tooltips[i])
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
            
    def load_expense(self, search_term=None):
        try:
            with sqlite3.connect("pos_database.db") as conn:
                cursor = conn.cursor()
                if search_term:
                    query = """
                        SELECT id, expense, description, expense_price, expense_date FROM expense
                        WHERE expense LIKE ? OR description LIKE ? OR expense_price LIKE ? OR expense_date LIKE ?
                        ORDER BY id DESC
                    """
                    search_term = f'%{search_term}%'
                    cursor.execute(query, (search_term,) * 4)
                else:
                    query = "SELECT id, expense, description, expense_price, expense_date FROM expense ORDER BY id DESC"
                    cursor.execute(query)
                records = cursor.fetchall()
                self.table.setRowCount(len(records))

                # Tooltips for columns
                tooltips = [
                    "Check to select this expense",
                    "Expense name/type",
                    "Description/details",
                    "The price/amount of this expense",
                    "Date when the expense was made"
                ]

                for index, row in enumerate(records):
                    expense_id = row[0]  # Store id

                    # Checkbox for selection
                    checkbox = QTableWidgetItem()
                    checkbox.setCheckState(Qt.CheckState.Unchecked)
                    checkbox.setToolTip(tooltips[0])
                    self.table.setItem(index, 0, checkbox)

                    # Set data and tooltip for each column
                    for col_index, data in enumerate(row[1:], 1):
                        if col_index == 3:  # Expense price column
                            # Show as int if possible
                            try:
                                data = int(data) if float(data).is_integer() else data
                            except Exception:
                                pass
                        item = QTableWidgetItem(str(data))
                        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                        # Tooltip for this cell
                        item.setToolTip(f"{tooltips[col_index]}: {data}")
                        self.table.setItem(index, col_index, item)

                    # If you want to store expense_id in a hidden column, uncomment below:
                    id_item = QTableWidgetItem(str(expense_id))
                    id_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                    id_item.setData(Qt.ItemDataRole.UserRole, expense_id)
                    self.table.setItem(index, 5, id_item)  # Hidden ID

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

    def open_add_inventory_dialog(self):
        dialog = AddInventoryDialog()
        if dialog.exec():
            self.load_expense()

    def delete_selected_expense(self):
        selected_rows = [i for i in range(self.table.rowCount()) if self.table.item(i, 0).checkState() == Qt.CheckState.Checked]
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "No expense selected for deletion.")
            return

        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        deleted_count = 0
        
        for row in selected_rows:
            exp_id = self.table.item(row, 4).data(Qt.ItemDataRole.UserRole)  # Get ID
            if exp_id:
                cursor.execute("DELETE FROM expense WHERE id = ?", (exp_id,))
                deleted_count += 1
        
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"Deleted {deleted_count} records successfully.")
        self.load_expense()



class AddInventoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Expense")
        self.setGeometry(300, 300, 400, 150)
        layout = QFormLayout(self)

        self.expense = QLineEdit()
        self.description = QLineEdit()
        self.expense_price = QLineEdit()
        self.expense_price = QLineEdit()  # Field for entering purchase price
        self.expense_date = QDateEdit()
        self.expense_date.setCalendarPopup(True)
        self.expense_date.setDate(QDate.currentDate())
        self.expense_date.setDisplayFormat("yyyy-MM-dd")

        layout.addRow("Expense:", self.expense)
        layout.addRow("Descrption:", self.description)
        layout.addRow("Expense Price:", self.expense_price)  # Add purchase price to the form
        layout.addRow("Expense Date", self.expense_date)

        self.submit_button = QPushButton("Add Expense")
        self.submit_button.clicked.connect(self.add_inventory)
        layout.addWidget(self.submit_button)

    def add_inventory(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        try:
            # Validate purchase price input
            try:
                expense_price = float(self.expense_price.text())
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for the expense price.")
                return  # Stop further processing if the input is invalid

            # Insert new inventory item, including validated purchase price
            cursor.execute(
                "INSERT INTO expense (expense, description, expense_price, expense_date) VALUES (?, ?, ?, ?)",
                (self.expense.text(), self.description.text(), expense_price, self.expense_date.date().toString("yyyy-MM-dd"))
            )
            
            conn.commit()
            QMessageBox.information(self, "Success", "Expense added successfully!")
            self.accept()
            
        except sqlite3.IntegrityError as e:
            QMessageBox.warning(self, "Error", f"Failed to update due to an error: {str(e)}")
        finally:
            conn.close()

