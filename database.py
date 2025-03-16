# database.py
import sqlite3

def initialize_db():
    conn = sqlite3.connect("pos_database.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        bike_name TEXT,
                        bike_model TEXT,
                        chassis_no TEXT UNIQUE,
                        reg_no TEXT,
                        client_name TEXT,
                        client_mobile TEXT,
                        client_cnic TEXT,
                        purchase_date TEXT DEFAULT (DATE('now')),
                        product_status TEXT DEFAULT 'Purchased')''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        client_cnic TEXT,
                        client_mobile TEXT,
                        inventory_id INTEGER,
                        sale_price REAL,
                        purchase_date TEXT,
                        sale_date TEXT,
                        payment_method TEXT,
                        profit REAL,
                        product_status TEXT DEFAULT 'Sold',
                        FOREIGN KEY (inventory_id) REFERENCES inventory(id))''')
    

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        client_name TEXT,
                        client_cnic TEXT,
                        client_mobile TEXT,
                        inventory_id INTEGER,
                        product_status TEXT,
                        purchase_date TEXT,
                        sale_date TEXT,
                        payment_method TEXT,
                        FOREIGN KEY (inventory_id) REFERENCES inventory(id))''')

    conn.commit()
    conn.close()
