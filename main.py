# main.py
import sys
from PyQt6.QtWidgets import QApplication
from home_page import HomePage
from sales import SalesPage
from users import UserManagementPage
from database import initialize_db

if __name__ == "__main__":
    initialize_db()
    app = QApplication(sys.argv)
    main_window = HomePage()
    main_window.show()
    sys.exit(app.exec())
