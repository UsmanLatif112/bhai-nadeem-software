import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
    QTableWidgetItem, QPushButton, QLabel, QLineEdit, QMessageBox, QHeaderView
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from users import UserManagementPage
# from sales import SalesPage
from user_data import UserPage
class UserManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(200, 200, 800, 600)
        self.connection = sqlite3.connect("pos_database.db")
        self.init_ui()

    def init_ui(self):
        # Main container for the window
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Gradient background
        central_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 lightgreen, stop:1 white
                );
            }
        """)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 1) Dark‐green header bar (logo + title)
        header_widget = self.create_header_bar()
        main_layout.addWidget(header_widget)

        # 2) Search widget (transparent background instead of a solid green bar)
        search_widget = self.create_search_widget()
        main_layout.addWidget(search_widget)

        # 3) Table for listing users
        self.table = self.setup_table()
        main_layout.addWidget(self.table)

        # 4) Button bar (bottom‐right)
        button_bar_layout = self.create_button_bar()
        main_layout.addLayout(button_bar_layout)

        # Finally, load user data
        self.load_users()

    # ------------------- HEADER BAR ------------------- #

    def create_header_bar(self):
        """
        Creates a top bar with a dark‐green background,
        containing the logo on the left and the title in the center.
        """
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(10)

        # Logo on the left
        logo_label = QLabel()
        logo_pixmap = QPixmap("BM_moters.png")
        logo_label.setPixmap(logo_pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation))
        header_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)

        # Title in the center
        header_text = QLabel("BISMILLAH MOTERS")
        header_text.setStyleSheet("color: white;")
        header_text.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        header_layout.addStretch(1)
        header_layout.addWidget(header_text, 0, Qt.AlignmentFlag.AlignVCenter)
        header_layout.addStretch(1)

        return header_widget

    # ------------------- SEARCH WIDGET ------------------- #

    def create_search_widget(self):
        """
        Creates a small bar below the header to hold the search box.
        The bar is transparent, so it won't appear as a separate green strip.
        """
        search_widget = QWidget()
        search_widget.setFixedHeight(50)
        
        # Make the widget transparent so it merges with the gradient
        search_widget.setStyleSheet("background-color: transparent;")

        layout = QHBoxLayout(search_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addStretch(1)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Users...")
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
        self.search_input.textChanged.connect(self.on_search)
        layout.addWidget(self.search_input)

        return search_widget

    # ------------------- TABLE & DATA METHODS ------------------- #

    def setup_table(self):
        """
        Table with columns:
        1) Select (checkbox)
        2) Client Name
        3) Client Mobile
        4) Client CNIC
        5) Date
        6) Manage (button)
        """
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "Select", "Client Name", "Client Mobile", "Client CNIC", "Date", "Manage"
        ])

        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #004d00;
                font-size: 14px;
                color: black;
                margin: 5px;
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

    def load_users(self, search_term=""):
        """
        Fetch user data from `usersmanagement` table and populate the table,
        searching by client_name, client_mobile, or client_cnic.
        """
        cursor = self.connection.cursor()
        query = """
            SELECT id,sales_id,inverted_id, client_name, client_mobile, client_cnic, date
            FROM usersmanagement
            WHERE client_name LIKE ? OR client_mobile LIKE ? OR client_cnic LIKE ?
        """
        like_input = f"%{search_term}%"
        cursor.execute(query, (like_input, like_input, like_input))
        records = cursor.fetchall()

        self.table.setRowCount(len(records))
        for row_index, (id,sales_id,inverted_id, name, mobile, cnic, date_str) in enumerate(records):
            # Checkbox
            checkbox_item = QTableWidgetItem()
            checkbox_item.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(row_index, 0, checkbox_item)

            # Data columns
            self.table.setItem(row_index, 1, QTableWidgetItem(name))
            self.table.setItem(row_index, 2, QTableWidgetItem(mobile))
            self.table.setItem(row_index, 3, QTableWidgetItem(cnic))
            self.table.setItem(row_index, 4, QTableWidgetItem(date_str))

            # Manage Button
            manage_btn = QPushButton("Manage")
            manage_btn.clicked.connect(lambda checked, user_id=sales_id,invertr_id=inverted_id: self.manage_user(user_id,invertr_id))
            self.table.setCellWidget(row_index, 5, manage_btn)
        
    # ------------------- SEARCH / MANAGE / DELETE ------------------- #

    def on_search(self, text):
        """
        Reloads the table data based on the search term.
        """
        self.load_users(text)

    def manage_user(self,user_id,invertr_id):
        # This method now opens the UserDetail page
        self.detail_window = UserPage(user_id,invertr_id)
        self.detail_window.show()
    def delete_selected_users(self):
        """
        Deletes all users whose "Select" checkbox is checked.
        Uses the columns to match the user in the database.
        """
        cursor = self.connection.cursor()
        rows_to_delete = []

        # Identify rows with checked checkboxes
        for row_index in range(self.table.rowCount()):
            checkbox_item = self.table.item(row_index, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.CheckState.Checked:
                # We can look up the unique combination of user info in the row.
                name  = self.table.item(row_index, 1).text()
                mobile= self.table.item(row_index, 2).text()
                cnic  = self.table.item(row_index, 3).text()
                date_ = self.table.item(row_index, 4).text()
                rows_to_delete.append((name, mobile, cnic, date_))

        if not rows_to_delete:
            QMessageBox.warning(self, "No Selection", "No users selected for deletion.")
            return

        deleted_count = 0
        for (name, mobile, cnic, date_) in rows_to_delete:
            try:
                cursor.execute("""
                    DELETE FROM usersmanagement
                    WHERE client_name=? AND client_mobile=? AND client_cnic=? AND date=?
                """, (name, mobile, cnic, date_))
                deleted_count += cursor.rowcount
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Database Error", str(e))

        self.connection.commit()
        self.load_users()
        QMessageBox.information(self, "Success", f"Deleted {deleted_count} user(s) successfully.")

    # ------------------- BOTTOM BUTTON BAR ------------------- #

    def create_button_bar(self):
        """
        Creates the horizontal layout at the bottom-right
        for the 'Delete Selected Users' button.
        """
        layout = QHBoxLayout()
        layout.addStretch(1)

        self.delete_button = QPushButton("Delete Selected Users")
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
        self.delete_button.clicked.connect(self.delete_selected_users)

        layout.addWidget(self.delete_button)
        layout.setContentsMargins(0, 0, 20, 20)
        return layout

    # ------------------- WINDOW CLOSE ------------------- #

    def closeEvent(self, event):
        """Close DB connection on window close."""
        self.connection.close()
        super().closeEvent(event)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserManagement()
    window.show()
    sys.exit(app.exec())
