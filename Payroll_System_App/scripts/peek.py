import sqlite3

conn = sqlite3.connect("payroll_vault.db")
cursor = conn.cursor()

print("🔍 Peeking into the Vault...\n")

# Get the first 5 unique Month/Year combinations
cursor.execute('SELECT DISTINCT "Payroll_Month", "Payroll_Year" FROM master_payroll LIMIT 5')
results = cursor.fetchall()

for row in results:
    month = row[0]
    year = row[1]
    print(f"Month: '{month}' | Year: '{year}' | Year Type: {type(year).__name__}")

conn.close()