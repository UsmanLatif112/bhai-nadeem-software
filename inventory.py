import sqlite3
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QDialog, QLineEdit, QFormLayout, QHeaderView
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class InventoryPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
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

        self.table = self.setup_table()
        main_layout.addWidget(self.table)

        button_bar_layout = self.create_button_bar()
        main_layout.addLayout(button_bar_layout)

        self.load_inventory()

    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")

        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(10)

        logo_label = QLabel()
        logo_pixmap = QPixmap("BM_moters.png")
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
        add_button = self.create_styled_button("Add New Inventory")
        add_button.clicked.connect(self.open_add_inventory_dialog)
        layout.addWidget(add_button)

        delete_button = self.create_styled_button("Delete Selected")
        delete_button.clicked.connect(self.delete_selected_inventory)
        layout.addWidget(delete_button)

        layout.addStretch()
        return layout

    def create_styled_button(self, text):
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
        button.setFixedSize(220, 50)
        return button

    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(9)  # Select + 8 data columns
        table.setHorizontalHeaderLabels([
            "Select", "ID", "Bike Name", "Bike Model",
            "Chassis No", "Reg No", "Client Name",
            "Purchase Date", "Status"
        ])
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #004d00;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #004d00;
                color: white;
                font-weight: bold;
            }
        """)
        return table

    def load_inventory(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, bike_name, bike_model, chassis_no, reg_no, client_name, purchase_date, product_status FROM inventory")
        records = cursor.fetchall()
        self.table.setRowCount(len(records))
        for index, row in enumerate(records):
            checkbox = QTableWidgetItem()
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            self.table.setItem(index, 0, checkbox)

            for col_index, data in enumerate(row):
                self.table.setItem(index, col_index + 1, QTableWidgetItem(str(data)))
        conn.close()

    def open_add_inventory_dialog(self):
        dialog = AddInventoryDialog()
        if dialog.exec():
            self.load_inventory()

    def delete_selected_inventory(self):
        selected_rows = [i for i in range(self.table.rowCount()) if self.table.item(i, 0).checkState() == Qt.CheckState.Checked]
        if not selected_rows:  # Corrected syntax here
            QMessageBox.warning(self, "No Selection", "No inventory selected for deletion.")
            return

        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        deleted_count = 0
        for row in selected_rows:
            inv_id = self.table.item(row, 1).text()
            cursor.execute("DELETE FROM inventory WHERE id = ?", (inv_id,))
            deleted_count += 1
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", f"Deleted {deleted_count} records successfully.")
        self.load_inventory()


class AddInventoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add New Inventory")
        self.setGeometry(300, 300, 400, 350)
        self.layout = QFormLayout(self)
        self.bike_name = QLineEdit()
        self.bike_model = QLineEdit()
        self.chassis_no = QLineEdit()
        self.reg_no = QLineEdit()
        self.client_name = QLineEdit()
        self.client_mobile = QLineEdit()
        self.client_cnic = QLineEdit()

        self.layout.addRow("Bike Name:", self.bike_name)
        self.layout.addRow("Bike Model:", self.bike_model)
        self.layout.addRow("Chassis No (Unique):", self.chassis_no)
        self.layout.addRow("Reg No (Optional):", self.reg_no)
        self.layout.addRow("Client Name:", self.client_name)
        self.layout.addRow("Client Mobile:", self.client_mobile)
        self.layout.addRow("Client CNIC:", self.client_cnic)

        self.submit_button = QPushButton("Add Inventory")
        self.submit_button.clicked.connect(self.add_inventory)
        self.layout.addWidget(self.submit_button)

    def add_inventory(self):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO inventory (bike_name, bike_model, chassis_no, reg_no, client_name, client_mobile, client_cnic) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.bike_name.text(), self.bike_model.text(), self.chassis_no.text(), self.reg_no.text(), self.client_name.text(), self.client_mobile.text(), self.client_cnic.text())
            )
            conn.commit()
            QMessageBox.information(self, "Success", "Inventory added successfully!")
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Chassis number already exists.")
        finally:
            conn.close()
