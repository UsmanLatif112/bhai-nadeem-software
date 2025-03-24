# database.py
import sqlite3

def initialize_db():
    conn = sqlite3.connect("pos_database.db")
    cursor = conn.cursor()

    # Initialize the inventory table with a new column for purchase price
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bike_name TEXT,
            bike_model TEXT,
            chassis_no TEXT UNIQUE,
            reg_no TEXT,
            client_name TEXT,
            client_mobile TEXT,
            client_cnic TEXT,
            purchase_date TEXT DEFAULT (DATE('now')),
            product_status TEXT DEFAULT 'Purchased',
            purchase_price REAL  
        )
    ''')

    # Initialize the sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            client_cnic TEXT,
            client_mobile TEXT,
            chassis_no TEXT,
            sale_price REAL,
            purchase_date TEXT DEFAULT (DATE('now')),
            sale_date TEXT DEFAULT (DATE('now')),
            payment_method TEXT,
            duration INTEGER,
            advance_payment REAL,
            monthly_installment REAL,
            remaining_amount REAL,
            profit REAL,
            purchase_price REAL,
            product_status TEXT DEFAULT 'Sold',
            FOREIGN KEY (chassis_no) REFERENCES inventory(chassis_no)
        )
    ''')
    
    # Initialize the users table with chassis_no directly
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            client_cnic TEXT,
            client_mobile TEXT,
            chassis_no TEXT,
            product_status TEXT,
            purchase_date TEXT,
            FOREIGN KEY (chassis_no) REFERENCES inventory(chassis_no)
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usersmanagement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT NOT NULL,
            client_mobile TEXT NOT NULL,
            client_cnic TEXT NOT NULL,
            date TEXT NOT NULL,
            sales_id INTEGER,
            inverted_id INTEGER
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
