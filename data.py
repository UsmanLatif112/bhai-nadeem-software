# import sqlite3

# conn = sqlite3.connect("pos_database.db")
# cursor = conn.cursor()

# try:
#     cursor.execute("ALTER TABLE sales ADD COLUMN invoice_number TEXT;")
# except sqlite3.OperationalError:
#     print("Column 'invoice_number' already exists.")

# try:
#     cursor.execute("ALTER TABLE sales ADD COLUMN installment_description TEXT;")
# except sqlite3.OperationalError:
#     print("Column 'installment_description' already exists.")

# conn.commit()
# conn.close()
# print("Columns added successfully!")


# import sqlite3

# # Example data
# chassis_list = ["Jf593060", "JF593070", "152065","ED072212","JF553095","EC831495","JF368908","JF041622","HA134446","HA052516","JF553025"]
# invoice_list = ["1077", "1075", "1074", "1070", "1068", "1087", "1109", "1071", "1078", "No invoice", "1067"]

# assert len(chassis_list) == len(invoice_list), "Lists must be the same length!"

# conn = sqlite3.connect("pos_database.db")
# cursor = conn.cursor()

# for chassis, invoice in zip(chassis_list, invoice_list):
#     cursor.execute(
#         "UPDATE sales SET invoice_number = ? WHERE chassis_no = ?",
#         (invoice, chassis)
#     )

# conn.commit()
# conn.close()
# print("Updated invoice numbers for all provided chassis numbers.")


import sqlite3

# Example data
chassis_list = ["Jf593060", "JF593070", "152065","ED072212","JF553095","EC831495","JF368908","JF041622","HA134446","HA052516","JF553025"]
desc_list = ["Clear amount on  1/05/2025", "None", "None", "None", "10/04/2025 15000 amount disount 15000 agr anhi deta to koi discount nahi pore 200000 qeemat ho gi", "150000 amount 01/06/2025 agr time pa aye payment to 15000 discount", "30000 amount 10/05/2025 - 30000 amount 10/07/2025 - 40000 amount 10/10/2025 - 40000 amount 10/01/2026", "20000 amount 15/01/2025 baki amount 8/04/2025 ko clear krni hy", "None", "None", "None"]

assert len(chassis_list) == len(desc_list), "Lists must be the same length!"

conn = sqlite3.connect("pos_database.db")
cursor = conn.cursor()

for chassis, desc in zip(chassis_list, desc_list):
    cursor.execute(
        "UPDATE sales SET installment_description = ? WHERE chassis_no = ?",
        (desc, chassis)
    )

conn.commit()
conn.close()
print("Updated descriptions for all provided chassis numbers.")
