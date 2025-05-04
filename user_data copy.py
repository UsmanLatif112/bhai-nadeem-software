import sqlite3
from PyQt6.QtWidgets import (QMessageBox,
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox,
    QHBoxLayout, QLabel, QLineEdit, QHeaderView, QApplication, QDialog, QFormLayout,QDateEdit, QCheckBox, QComboBox
)
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView


from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton
from PyQt6.QtGui import QPixmap, QFont,QImage
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QFont,QTextDocument,QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox 
import os,sys
from Instalment import Installment_pages


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and frozen """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
     
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
        
    def open_installment_page(self, chassis_no):
        # Assuming Installment_pages takes chassis_no as an initializer argument
        self.installment_page = Installment_pages(chassis_no)
        self.installment_page.show()

    def create_header(self):
        header_widget = QWidget()
        header_widget.setFixedHeight(80)
        header_widget.setStyleSheet("background-color: #004d00;")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(10, 10, 10, 10)
        
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
        table.setColumnCount(16)  # Increase column count by one for the checkbox
        
        headers = [
            "Select", 
            "Client\nName", 
            "Client\nMobile\nNo", 
            "Client\nCNIC", 
            "Bike\nChassis\nNo", 
            "Purchase\nPrice", 
            "Sale\nPrice", 
            "Date", 
            "Product\nStatus", 
            "Payment\nMethod", 
            "Remaining\nAmount", 
            "Duration", 
            "Advance\nPayment", 
            "Monthly\nInstallment", 
            "Action",
            "View"
            "Action"
        ]
        
        tooltips = [
           "Select", 
            "Client Name", 
            "Client Mobile No", 
            "Client CNIC", 
            "Bike Chassis No", 
            "Purchase Price", 
            "Sale Price", 
            "Date", 
            "Product Status", 
            "Payment Method", 
            "Remaining Amount", 
            "Duration", 
            "Advance Payment", 
            "Monthly Installment", 
            "Action",
            "view"
            "Action"
        ]

        # Set horizontal header labels
        table.setHorizontalHeaderLabels(headers)

        # Set tooltips for each header item
        for i in range(len(headers)):
            item = QTableWidgetItem(headers[i])
            item.setToolTip(tooltips[i])  # Setting tooltip on the header item
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

    def load_sales(self, search_term=""):
        """ Fetch product details from the sales table based on user_id and display them in the frontend table. """
        self.connection = sqlite3.connect("pos_database.db")
        cursor = self.connection.cursor()

        client_cnic = None  # Initialize client_cnic

        # Fetch CNIC from sales table
        if self.user_id:
            cursor.execute("SELECT client_cnic FROM sales WHERE id = ?", (self.user_id,))
            result = cursor.fetchone()
            if result:
                client_cnic = result[0]

        # If no valid CNIC found in sales, check inventory for CNIC
        if (not client_cnic or client_cnic == "0") and self.invertr_id:
            cursor.execute("SELECT client_cnic FROM inventory WHERE id = ?", (self.invertr_id,))
            result = cursor.fetchone()
            if result:
                client_cnic = result[0]

        # Fallback to client name if CNIC is invalid or zero
        if not client_cnic or client_cnic == "0":
            cursor.execute("SELECT client_name FROM inventory WHERE id = ?", (self.invertr_id,))
            result = cursor.fetchone()
            if result:
                client_name = result[0]
                where_clause = "WHERE client_name = ?"
                params = [client_name]
            else:
                # Handle the case where no client_name could be found
                self.connection.close()
                return  # Exit the function as no valid identifier is available
        else:
            where_clause = "WHERE client_cnic = ?"
            params = [client_cnic]

        if search_term:
            where_clause += " AND (client_name = ? OR client_mobile = ? OR chassis_no = ? OR client_cnic = ?)"
            params.extend([search_term] * 4)  # Use exact search term for each field

        # Query to fetch sales data
        query_sales = f"""
            SELECT client_name, client_mobile, client_cnic, chassis_no, 'None' AS purchase_price, sale_price,
                sale_date, product_status, payment_method, remaining_amount, duration, advance_payment, 
                monthly_installment
            FROM sales 
            {where_clause}
            ORDER BY id DESC
        """

        # Query to fetch inventory data
        query_inventory = f"""
            SELECT client_name, client_mobile, client_cnic, chassis_no, purchase_price, '0' AS sale_price,
                purchase_date, product_status, 'None' AS payment_method, '0' AS remaining_amount, 
                '0' AS duration, '0' AS advance_payment, '0' AS monthly_installment
            FROM inventory 
            {where_clause}
            ORDER BY id DESC
        """

        # Execute queries
        cursor.execute(query_sales, params)
        records_sales = cursor.fetchall()
        cursor.execute(query_inventory, params)
        records_inventory = cursor.fetchall()

        # Combine and display all records
        all_records = records_sales + records_inventory
        self.connection.close()
        self.table.setRowCount(0)  
        if all_records:
            self.table.setRowCount(len(all_records)) 
            tooltips = [
            "Select",
            "Client Name",
            "Client Mobile No",
            "Client CNIC",
            "Bike Chassis No",
            "Purchase Price",
            "Sale Price",
            "Date",
            "Product Status",
            "Payment Method",
            "Remaining Amount",
            "Duration",
            "Advance Payment",
            "Monthly Installment",
            "Action",
            "View"
        ]

        for row_idx, row_data in enumerate(all_records):
            checkbox = QTableWidgetItem()
            checkbox.setCheckState(Qt.CheckState.Unchecked)
            checkbox.setToolTip(tooltips[0])
            self.table.setItem(row_idx, 0, checkbox)

            for col_idx, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                # Assign tooltip, +1 because col 0 is checkbox
                if (col_idx+1) < len(tooltips):
                    # item.setToolTip(tooltips[col_idx+1])
                    item.setToolTip(f"{tooltips[col_idx+1]}: {col_data}")

                self.table.setItem(row_idx, col_idx+1, item)
            # Set tooltips for action/view buttons as well
            if row_data[8] not in [None, 'None', '', 'net cash', 'Net Cash', 'NET CASH']:
                manage_btn = QPushButton("Manage")
                manage_btn.setToolTip("Open payment management dialog")
                manage_btn.clicked.connect(lambda _, sale_id=row_data[3]: self.open_new_sale_dialog(sale_id))
                self.table.setCellWidget(row_idx, 14, manage_btn)
                
                view_btn = QPushButton("View")
                view_btn.setToolTip("View installment page")
                view_btn.clicked.connect(lambda _, chassis_no=row_data[3]: self.open_installment_page(chassis_no))
                self.table.setCellWidget(row_idx, 15, view_btn)

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
        printer = QPrinter()
        printer.setResolution(900)
        print_dialog = QPrintDialog(printer, self)
        
        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            painter = QPainter(printer)
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            y_offset = 40
            line_height = 40
            
            # Load the image specifically for this function
            logo_image_path = resource_path('BM_moters_b.png')
            logo_image = QImage(logo_image_path)
            if logo_image.isNull():
                print("Failed to load image for printing:", logo_image_path)  # Debug output
                return
            
            logo_width = 500
            logo_height = 50
            # Draw the image
            painter.drawImage(100, y_offset, logo_image.scaled(logo_width, logo_height, Qt.AspectRatioMode.KeepAspectRatio))
            y_offset += logo_height + 10

            y_offset += line_height
            painter.drawText(100, y_offset, "-" * 50)  # Separator line
            y_offset += line_height
            for row in selected_rows:
                self.connection = sqlite3.connect("pos_database.db")
                cursor = self.connection.cursor()

                chassis_no = row['Chassis No']
                cursor.execute("SELECT bike_name, bike_model FROM inventory WHERE chassis_no = ?", (chassis_no,))
                bike_data = cursor.fetchone()
                bike_name = bike_data[0] if bike_data else "Unknown"
                bike_model = bike_data[1] if bike_data else "Unknown"

                # Get latest payment for this chassis_no (from payments table)
                cursor.execute("""
                    SELECT payment_amount
                    FROM payments
                    WHERE chassis_no = ?
                    ORDER BY payment_date DESC, id DESC
                    LIMIT 1
                """, (chassis_no,))
                payment_row = cursor.fetchone()
                add_payment = payment_row[0] if payment_row and payment_row[0] not in (None, '', 0, '0', 'None') else None

                # Get discount from sales table
                cursor.execute("SELECT discount FROM sales WHERE chassis_no = ?", (chassis_no,))
                discount_row = cursor.fetchone()
                discount = discount_row[0] if discount_row and discount_row[0] not in (None, '', 0, '0', 'None') else None

                painter.drawText(100, y_offset, f"User Name:  {row['Client Name']}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Mobile No:  {row['Mobile No']}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"CNIC:        {row['CNIC']}")
                y_offset += line_height
                painter.drawText(100, y_offset, "-" * 50)
                y_offset += line_height
                painter.drawText(100, y_offset, f"Bike Name:  {bike_name}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Bike Model:  {bike_model}")
                y_offset += line_height
                painter.drawText(100, y_offset, f"Chassis No:  {chassis_no}")
                y_offset += line_height
                painter.drawText(100, y_offset, "-" * 50)
                y_offset += line_height
                if row.get('Payment Method') not in (None, '', 'None'):
                    painter.drawText(100, y_offset, f"Payment Method: {row['Payment Method']}")
                    y_offset += line_height

                painter.drawText(100, y_offset, f"Sale Price:  {row['Sale Price']}")
                y_offset += line_height
                
                # Remaining Amount
                if row['Remaining Amount'] not in (None, '', '0', '0.0', 0, 0.0, 'None'):
                    painter.drawText(100, y_offset, f"Remaining Amount: {row['Remaining Amount']}")
                    y_offset += line_height

                # Monthly Installment
                if row['Monthly Installment'] not in (None, '', '0', '0.0', 0, 0.0, 'None'):
                    painter.drawText(100, y_offset, f"Monthly Installment: {row['Monthly Installment']}")
                    y_offset += line_height

                # Duration
                if row['Duration'] not in (None, '', '0', 0, 'None'):
                    painter.drawText(100, y_offset, f"Duration: {row['Duration']}")
                    y_offset += line_height

                if add_payment is not None:
                    painter.drawText(100, y_offset, f"Add Payment: {add_payment}")
                    y_offset += line_height
                    
                if discount is not None:
                    painter.drawText(100, y_offset, f"Discount: {discount}")
                    y_offset += line_height

                painter.drawText(100, y_offset, "-" * 50)
                y_offset += line_height
                font.setBold(True)
                painter.setFont(font)
                painter.drawText(100, y_offset, "Shop# 46 Jinnah Market, Multan Road, Rasool Pura Mailsi, Punjab Pakistan.")
                y_offset += line_height
                painter.drawText(100, y_offset, "Ch Nadeem 03007582812, Ch Raheel 03007777221")
                y_offset += line_height

                cursor.close()
                self.connection.close()

            painter.end()


    
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
        cursor.execute("SELECT chassis_no,client_name, monthly_installment,duration,remaining_amount FROM sales WHERE chassis_no = ?", (row_id,))
        result = cursor.fetchone()
        connection.close()
        chassis_no = result[0]
        client_name = result[1]
        monthly_installment = result[2]
        duration = result[3]
        remaining_amount = result[4]
        dialog = NewSaleDialog(chassis_no,client_name, monthly_installment, duration, remaining_amount, parent=self)
        dialog.exec()


class NewSaleDialog(QDialog):
    def __init__(self, chassis_no, client_name, monthly_installment, duration, remaining_amount, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Update Payments")
        self.setGeometry(300, 200, 400, 250)
        layout = QFormLayout(self)

        # Fields
        self.chassis_no = QLineEdit(chassis_no)
        self.chassis_no.setReadOnly(True)
        self.client_name = QLineEdit(client_name)
        self.client_name.setReadOnly(True)
        self.duration = QComboBox()
        self.duration.addItems([str(i) for i in range(1, 13)])
        self.duration.setCurrentText(str(duration))
        self.monthly_installment = QLineEdit(str(monthly_installment))
        self.monthly_installment.setReadOnly(True)
        self.remaining_amount = QLineEdit(str(int(remaining_amount)))
        self.remaining_amount.setReadOnly(True)
        self.payment_no = QLineEdit()
        self.discount = QLineEdit()
        self.discount.setPlaceholderText("Optional")

        # Layout
        layout.addRow("Chassis No:", self.chassis_no)
        layout.addRow("Client Name:", self.client_name)
        layout.addRow("Duration (Months):", self.duration)
        layout.addRow("Monthly Installment:", self.monthly_installment)
        layout.addRow("Remaining Amount:", self.remaining_amount)
        layout.addRow("Add Payment:", self.payment_no)
        layout.addRow("Discount:", self.discount)

        self.remaining_amount_previous = int(remaining_amount)
        self.monthly_installment_previous = str(monthly_installment)

        self.payment_no.textChanged.connect(self.calculate_installments)
        self.discount.textChanged.connect(self.calculate_installments)

        self.submit_button = QPushButton("Update Payment")
        self.submit_button.clicked.connect(self.submit_sale)
        layout.addWidget(self.submit_button)

    def calculate_installments(self):
        """Update remaining and monthly installment, factoring in discount."""
        try:
            payment_text = self.payment_no.text()
            payment_amount = int(payment_text) if payment_text.strip() else 0
            discount_text = self.discount.text()
            discount_amount = int(discount_text) if discount_text.strip() else 0

            new_remaining_amount = self.remaining_amount_previous - payment_amount - discount_amount
            if new_remaining_amount < 0:
                new_remaining_amount = 0
            self.remaining_amount.setText(str(new_remaining_amount))

            duration = int(self.duration.currentText())
            new_monthly_installment = new_remaining_amount // duration if duration > 0 else new_remaining_amount
            self.monthly_installment.setText(str(new_monthly_installment))
        except ValueError:
            self.remaining_amount.setText(str(self.remaining_amount_previous))
            self.monthly_installment.setText(self.monthly_installment_previous)

    def submit_sale(self):
        """Update payments and discount in database, and update profit as per new sale price."""
        payment_text = self.payment_no.text().strip()
        if not payment_text or float(payment_text) == 0:
            QMessageBox.warning(self, "Input Error", "Please add a payment before submitting.")
            return  # Prevents further execution

        payment_amount = float(payment_text)
        discount_amount = float(self.discount.text()) if self.discount.text() else 0
        payment_date = QDate.currentDate().toString("yyyy-MM-dd")
        chassis_no = self.chassis_no.text()
        client_name = self.client_name.text()
        duration = int(self.duration.currentText())
        monthly_installment = float(self.monthly_installment.text())
        remaining_amount = float(self.remaining_amount.text())

        try:
            connection = sqlite3.connect("pos_database.db")
            cursor = connection.cursor()
            # Get current sale_price and purchase_price
            cursor.execute("SELECT sale_price, purchase_price FROM sales WHERE chassis_no = ?", (chassis_no,))
            result = cursor.fetchone()
            sale_price = float(result[0]) if result and result[0] not in (None, '', 'None') else 0
            purchase_price = float(result[1]) if result and result[1] not in (None, '', 'None') else 0

            new_sale_price = sale_price - discount_amount
            profit = new_sale_price - purchase_price

            cursor.execute("""
                UPDATE sales
                SET duration = ?, monthly_installment = ?, remaining_amount = ?, discount = ?, sale_price = ?, profit = ?
                WHERE chassis_no = ?
            """, (duration, monthly_installment, remaining_amount, discount_amount, new_sale_price, profit, chassis_no))

            cursor.execute("""
                INSERT INTO payments (client_name, chassis_no, payment_amount, payment_date)
                VALUES (?, ?, ?, ?)
            """, (client_name, chassis_no, payment_amount, payment_date))

            connection.commit()
            connection.close()
            QMessageBox.information(self, "Submitted", "Sale details, payment, discount, and profit updated successfully.")
            self.parent().load_sales()
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Failed to update sale details: {str(e)}")



if __name__ == "__main__":
    app = QApplication([])
    window = UserPage()
    window.show()
    app.exec()
