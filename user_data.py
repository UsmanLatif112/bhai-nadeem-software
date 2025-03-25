import sqlite3
from PyQt6.QtWidgets import (QMessageBox,
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QHBoxLayout, QLabel, QLineEdit, QHeaderView, QApplication, QDialog, QFormLayout,QDateEdit, QCheckBox, QComboBox
)
from PyQt6.QtGui import QPixmap, QFont,QImage
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QFont,QTextDocument,QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox  
class UserPage(QWidget):
    def __init__(self,user_id,invertr_id):
        super().__init__()
        self.user_id = user_id
        self.invertr_id = invertr_id 
        self.setWindowTitle("User Management")
        self.setGeometry(200, 200, 900, 500)
        self.connection = sqlite3.connect("pos_database.db")
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        header_widget = self.create_header()
        self.layout.addWidget(header_widget)
        self.search_bar_layout = self.create_search_bar()
        self.layout.addLayout(self.search_bar_layout)

        self.table = self.setup_table()
        self.layout.addWidget(self.table)

        button_bar_layout = self.create_button_bar()
        self.layout.addLayout(button_bar_layout)
        self.load_sales()

    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        logo_label = QLabel()
        logo_pixmap = QPixmap("BM_moters.png")
        logo_label.setPixmap(logo_pixmap.scaledToHeight(60, Qt.TransformationMode.SmoothTransformation))
        header_layout.addWidget(logo_label, 0, Qt.AlignmentFlag.AlignVCenter)
        header_text = QLabel("Users Management")
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
        self.search_input.setPlaceholderText("Search Sales...")
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
        self.search_input.textChanged.connect(self.load_sales)
        layout.addWidget(self.search_input)

        layout.setContentsMargins(0, 0, 20, 0)

        return layout

    def create_button_bar(self):
        layout = QHBoxLayout()
        layout.addStretch(1)

        self.add_sale_button = QPushButton("Print")
        self.add_sale_button.clicked.connect(self.print_selected_sale)
        self.add_sale_button.setStyleSheet("""
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
        self.add_sale_button.setFixedSize(200, 30)
        layout.addWidget(self.add_sale_button)
        
        layout.setContentsMargins(0, 0, 20, 20)

        return layout

    def setup_table(self):
        table = QTableWidget()
        table.setColumnCount(15)  # Increase column count by one for the checkbox
        table.setHorizontalHeaderLabels([
            "Select", "Client Name", "Client Mobile No", "Client CNIC", "Bike Chassis No", "Purchase Price", "Sale Price", 
            "Date","Product Status", "Payment Method", "Remaining Amount", "Duration", "Advance Payment", "Monthly Installment", "Action"
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


    def load_sales(self,search_term=""):
        """ Fetch product details from the sales table based on user_id and display them in the frontend table. """
        self.connection = sqlite3.connect("pos_database.db")
        cursor = self.connection.cursor()
        if self.user_id:
            cursor.execute("SELECT client_cnic FROM sales WHERE id = ?", (self.user_id,))
            result = cursor.fetchone()
            if result:
                client_cnic = result[0]
        if self.invertr_id:  # If no CNIC found in sales, check inventory
            cursor.execute("SELECT client_cnic FROM inventory WHERE id = ?", (self.invertr_id,))
            result = cursor.fetchone()
            if result:
                client_cnic = result[0]
        where_clause = f"WHERE client_cnic = ?"
        params = [client_cnic]
        if search_term:
            where_clause += f" AND (client_name LIKE ? OR client_mobile LIKE ? OR chassis_no LIKE ? OR client_cnic LIKE ?)"
            params.extend(['%' + search_term + '%'] * 4)  # Append search term for client_name, client_mobile, and chassis_no

        # Query to fetch sales data
        query_sales = f"""
            SELECT client_name, client_mobile, client_cnic, chassis_no, 'None' AS purchase_price, sale_price,
                sale_date, product_status, payment_method, remaining_amount, duration, advance_payment, 
                monthly_installment
            FROM sales
            {where_clause}
        """
        
        # Query to fetch inventory data
        query_inventory = f"""
            SELECT client_name, client_mobile, client_cnic, chassis_no, purchase_price, 'None' AS sale_price,
                purchase_date, product_status, 'None' AS payment_method, 'None' AS remaining_amount, 
                'None' AS duration, 'None' AS advance_payment, 'None' AS monthly_installment
            FROM inventory
            {where_clause}
        """

        # Execute queries with the CNIC as parameter and the search term
        cursor.execute(query_sales, params)
        records_sales = cursor.fetchall()
        cursor.execute(query_inventory, params)
        records_inventory = cursor.fetchall()

        # Store all records (sales + inventory) in the local variable
        all_records = records_sales + records_inventory
        self.connection.close()
        self.table.setRowCount(0)  
        if all_records:
            self.table.setRowCount(len(all_records)) 
            for row_idx, row_data in enumerate(all_records):
                checkbox = QTableWidgetItem()
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                self.table.setItem(row_idx, 0, checkbox)

                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.table.setItem(row_idx, col_idx + 1, item)
                if row_data[8] not in [None,'None','','net cash','Net Cash','NET CASH']:
                    manage_btn = QPushButton("Manage")
                    manage_btn.clicked.connect(lambda _, sale_id=row_data[3] : self.open_new_sale_dialog(sale_id))
                    self.table.setCellWidget(row_idx, 14, manage_btn)


        self.connection.close()

    def delete_selected_sale(self):
        # import pdb;pdb.set_trace()
        selected_row = self.table.currentRow()
        if selected_row != -1:
            chassis_no = self.table.item(selected_row, 3).text()
            self.delete_sale(chassis_no)

   

    def print_selected_sale(self):
        selected_rows = []
        for row in range(self.table.rowCount()):
            checkbox_item = self.table.item(row, 0)  # Index 0 for checkbox column
            if checkbox_item.checkState() == Qt.CheckState.Checked:
                # import pdb;pdb.set_trace()
                client_name = self.table.item(row, 1).text()  # Client Name
                mobile_no = self.table.item(row, 2).text()    # Mobile No
                cnic = self.table.item(row, 3).text()          # CNIC
                chassis_no = self.table.item(row, 4).text()    # Chassis No
                sale_price = self.table.item(row, 5).text()    # Purchase Price
                sale_price = self.table.item(row, 6).text()    # Sale Price
                date = self.table.item(row, 7).text()           # Date
                product_status = self.table.item(row, 8).text() # Product Status
                payment_method = self.table.item(row, 9).text() # Product Status
                remaining_Amount = self.table.item(row, 10).text() # Product Status
                duration = self.table.item(row, 11).text() # Product Status
                Monthly_Installment = self.table.item(row, 13).text() # Product Status
                if len(selected_rows)==0:
                    selected_rows.append({
                        "Client Name": client_name,
                        "Mobile No": mobile_no,
                        "CNIC": cnic,
                        "Chassis No": chassis_no,
                        "Sale Price": sale_price,
                        "Date": date,
                        "Product Status": product_status,
                        "Payment Method": payment_method,
                        "Remaining Amount": remaining_Amount,
                        "Duration": duration,
                        "Monthly Installment": Monthly_Installment

                    })

        if selected_rows:
            # Call the show_print_preview function and pass selected_rows
            self.show_print_preview(selected_rows)
        else:
            QMessageBox.warning(self, "No Selection", "Please select at least one sale to print.")

    def show_print_preview(self, selected_rows):
        # Set up the printer
        printer = QPrinter()
        printer.setResolution(900)  # Set high resolution (e.g., 900 DPI)
        
        print_dialog = QPrintDialog(printer, self)

        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            painter = QPainter(printer)
            font = QFont()
            font.setPointSize(10) 
            painter.setFont(font)
            y_offset = 40 
            line_height = 40  
            logo_image = QImage("BM_moters_b.png")
            if logo_image.isNull():
                print("Failed to load image.")
                return
            logo_width = 500
            logo_height = 50
            # Draw the image with the correct aspect ratio mode
            painter.drawImage(100, y_offset, logo_image.scaled(logo_width, logo_height))
            y_offset += logo_height + 10 

            y_offset += line_height
            painter.drawText(100, y_offset, "-" * 50)  # Separator line
            y_offset += line_height
            # Print each selected row
            for row in selected_rows:
                painter.drawText(100, y_offset, f"User Name:  {row['Client Name']}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Mobile No:  {row['Mobile No']}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"CNIC:        {row['CNIC']}")
                y_offset += line_height
                painter.drawText(100, y_offset, "-" * 50)  # Separator line
                y_offset += line_height
                painter.drawText(100, y_offset, f"Bike Name:  ssss")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Bike Model:  ssss")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Chassis No:  {row['Chassis No']}")
                y_offset += line_height
                painter.drawText(100, y_offset, "-" * 50)  # Separator line
                y_offset += line_height
                painter.drawText(100, y_offset, f"Sale Price:  {row['Sale Price']}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Remaining Amount: {row['Remaining Amount']}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Monthly Installment: {row['Monthly Installment']}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Duration: {row['Duration']}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Add Payment: 100")
                y_offset += line_height
                painter.drawText(100, y_offset, "-" * 50)  # Separator line
                y_offset += line_height
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(100, y_offset, f"Shop# 46 Jinnah Market, Multan Road, Rasool Pura Mailsi, Punjab Pakistan.")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Ch Nadeem 03007582812, Ch Raheel 03007777221")
                y_offset += line_height
            painter.end()  # End the painting process

    
    def delete_sale(self, chassis_no):
        conn = sqlite3.connect("pos_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sales WHERE chassis_no = ?", (chassis_no,))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "User record deleted successfully!")
        self.load_sales()

    def open_new_sale_dialog(self,row_id):
        connection = sqlite3.connect("pos_database.db")
        cursor = connection.cursor()
        cursor.execute("SELECT chassis_no,monthly_installment,duration,remaining_amount FROM sales WHERE chassis_no = ?", (row_id,))
        result = cursor.fetchone()
        connection.close()

        chassis_no = result[0]
        monthly_installment = result[1]
        duration = result[2]
        remaining_amount = result[3]
        dialog = NewSaleDialog(chassis_no, monthly_installment, duration, remaining_amount, parent=self)
        dialog.exec()
class NewSaleDialog(QDialog):
    def __init__(self, chassis_no, monthly_installment, duration, remaining_amount, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Payments")
        self.setGeometry(300, 300, 400, 200)
        layout = QFormLayout(self)
        # Create input fields
        self.chassis_no = QLineEdit()
        self.chassis_no.setText(chassis_no)
        self.chassis_no.setReadOnly(True)

        self.duration = QComboBox()
        self.duration.addItems([str(i) for i in range(1, 13)])  # 1 to 12 months
        # Assuming duration, monthly_installment, and remaining_amount are already defined as floats
        self.duration.setCurrentText(str(duration))
        self.monthly_installment = QLineEdit()
        self.monthly_installment.setText(str(int(monthly_installment)))  # Convert to integer
        self.monthly_installment.setReadOnly(True)
        self.remaining_amount = QLineEdit()
        self.remaining_amount.setText(str(int(remaining_amount)))  # Convert to integer
        self.remaining_amount.setReadOnly(True)

        self.payment_no = QLineEdit()

        # Add the widgets to the layout
        layout.addRow("Chassis No:", self.chassis_no)
        layout.addRow("Duration (Months):", self.duration)
        layout.addRow("Monthly Installment:", self.monthly_installment)
        layout.addRow("Remaining Amount:", self.remaining_amount)
        layout.addRow("Add Payment:", self.payment_no)
        self.original_monthly_installment_previous = monthly_installment
        self.original_remaining_amount_previous = remaining_amount
        self.payment_no.textChanged.connect(self.calculate_installments)
        self.submit_button = QPushButton("Update Payment")
        self.submit_button.clicked.connect(self.submit_sale)
        layout.addWidget(self.submit_button)
    def calculate_installments(self):
        try:
            add_payment = int(self.payment_no.text() if self.payment_no.text() else 0)  # Added payment
            months = int(self.duration.currentText())  # Get selected duration value
            remaining = float(self.remaining_amount.text() if self.remaining_amount.text() else 0)  # Get remaining amount
            # import pdb;pdb.set_trace()

            if add_payment:  # Proceed only if there's an added payment
                # Subtract added payment from remaining amount
                updated_remaining = int(remaining - add_payment)
                
                # Ensure updated_remaining is not negative
                if updated_remaining < 0:
                    updated_remaining = 0
                
                # Calculate the new monthly installment based on the updated remaining amount
                monthly = updated_remaining / months if months > 0 else 0
                
                # Update the UI with the new values
                self.monthly_installment.setText(f"{monthly:.2f}")
                self.remaining_amount.setText(f"{updated_remaining:.2f}")
            else:
                # If no additional payment, reset to original values
                self.remaining_amount.setText(f"{self.original_remaining_amount_previous:.2f}")
                self.monthly_installment.setText(f"{self.original_monthly_installment_previous:.2f}")

        except Exception as e:
            print(f"An error occurred: {e}")  # Handle exception

    def submit_sale(self):
        # Get the current values from the dialog
        chassis_no = self.chassis_no.text()
        duration = int(self.duration.currentText())
        monthly_installment = float(self.monthly_installment.text())
        remaining_amount = float(self.remaining_amount.text())
        print(self.payment_no.text(),'----------')
        try:
            connection = sqlite3.connect("pos_database.db")  # Replace with the actual database file path
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE sales
                SET duration = ?,add_payment=?, monthly_installment = ?, remaining_amount = ?
                WHERE chassis_no = ?
            """, (duration,self.payment_no.text(), monthly_installment, remaining_amount, chassis_no))
            connection.commit()
            connection.close()
            QMessageBox.information(self, "Submitted", "Sale details updated successfully.")
            self.parent().load_sales()
            self.accept()  # Close the dialog

        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Failed to update sale details: {str(e)}")


if __name__ == "__main__":
    app = QApplication([])
    window = UserPage()
    window.show()
    app.exec()
