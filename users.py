import sqlite3
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QLineEdit, QFormLayout, QHeaderView, QApplication
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class UserManagementPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("User Management")
        self.setGeometry(200, 200, 800, 600)
        self.connection = sqlite3.connect("pos_database.db")
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

        self.load_users()

    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(10)

        logo_label = QLabel()
        logo_pixmap = QPixmap("BM_moters.png")
        logo_label.setPixmap(logo_pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation))
        header_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)

        header_text = QLabel("BISMILLAH MOTERS")
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

        layout.setContentsMargins(0, 0, 20, 0)

        return layout

    def create_button_bar(self):
        layout = QHBoxLayout()
        layout.addStretch(1)  # This pushes the button to the right

        delete_button = QPushButton("Delete Selected Users")
        delete_button.clicked.connect(self.delete_selected_users)
        delete_button.setStyleSheet("""
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
        delete_button.setFixedSize(200, 30)  # Ensure consistent dimensions

        layout.addWidget(delete_button)
        layout.setContentsMargins(0, 0, 20, 20)  # Right and bottom padding

        return layout

    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Select", "Client Name", "Client CNIC", "Client Mobile", "Chassis No", "Status", "Date"
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

    def load_users(self, search_term=""):
        self.connection = sqlite3.connect("pos_database.db")  # Ensure connection is refreshed each time
        cursor = self.connection.cursor()
        query = """
            SELECT client_name, client_cnic, client_mobile, chassis_no, purchase_date,purchase_date FROM users
            WHERE client_name LIKE ? OR client_cnic LIKE ? OR client_mobile LIKE ? OR chassis_no LIKE ?
        """
        cursor.execute(query, ('%'+search_term+'%',)*4)
        records = cursor.fetchall()
        self.table.setRowCount(len(records))
        for index, row in enumerate(records):
            checkbox = QTableWidgetItem()
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(index, 0, checkbox)
            for col_index, data in enumerate(row):
                item = QTableWidgetItem(str(data))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(index, col_index + 1, item)
            # Manually set the "Status" column to "Purchased"
            status_item = QTableWidgetItem("Purchased")
            status_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.table.setItem(index, 5, status_item)  # Assuming "Status" is the sixth column
        self.connection.close()



    def on_search(self, text):
        self.load_users(text)

    def delete_selected_users(self):
        # Reopen the connection
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()

        selected_rows = [index for index in range(self.table.rowCount()) if self.table.item(index, 0).checkState() == Qt.CheckState.Checked]
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "No users selected for deletion.")
            return

        try:
            for row in selected_rows:
                user_id = self.table.item(row, 1).text()
                cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            QMessageBox.information(self, "Success", f"Deleted {len(selected_rows)} users successfully.")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Database Error", str(e))
        finally:
            self.load_users()  # Reload the user data
            conn.close() 

    def closeEvent(self, event):
        self.connection.close()

if __name__ == "__main__":
    app = QApplication([])
    window = UserManagementPage()
    window.show()
    app.exec()
