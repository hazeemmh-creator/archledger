import sqlite3

# 1. Create and connect to the new database file (The Vault)
print("Opening the forge...")
conn = sqlite3.connect('payroll_vault.db')
cursor = conn.cursor()

# 2. Write the blueprint for our Master Table
print("Building the Master Payroll table...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS master_payroll (
    "Txn_ID" TEXT PRIMARY KEY,
    "Payroll_Month" INTEGER,
    "Payroll_Year" INTEGER,
    "STAFF NAME" TEXT,
    "DESIGNATION" TEXT,
    "GRADE LEVEL" TEXT,
    "BASIC SALARY" REAL,
    "ALLCE/ AREARS" REAL,
    "RESEARCH ALLOWANCE" REAL,
    "HARDSHIP ALLOWANCE" REAL,
    "LEGISLATIVE DUTY ALLOWANCE" REAL,
    "GROSS SALARY" REAL,
    "AUCTION" REAL,
    "COOP 1 CONTR/SPEC SAVINGS" REAL,
    "COOP 1 LOAN RECOVERY" REAL,
    "COOP 2 CONTR/SPEC SAVINGS" REAL,
    "COOP 2 LOAN RECOVERY" REAL,
    "NHF DED." REAL,
    "PAYE" REAL,
    "EMPLOYEE PENSIONS" REAL,
    "TOTAL DEDUCTION" REAL,
    "PREVIOUS MONTH" REAL,
    "NET PAY" REAL
)
''')

# 3. Save the changes and lock the vault
conn.commit()
conn.close()

print("Gbosa! The SQLite Database Vault has been successfully created with the perfect schema!")