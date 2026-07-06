import sqlite3

conn = sqlite3.connect("payroll_vault.db")
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(master_payroll)")

columns = [info[1] for info in cursor.fetchall()]
print("\n=== THE EXACT DATABASE COLUMNS ===")
print(columns)
print("==================================\n")

conn.close()