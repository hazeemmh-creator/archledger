import sqlite3

def run_patch():
    print("⏳ Applying COOP 2 LOAN RECOVERY Patch...")
    conn = sqlite3.connect("payroll_vault.db")
    cursor = conn.cursor()

    # 1. Ensure the column exists
    try:
        cursor.execute('ALTER TABLE master_payroll ADD COLUMN "COOP 2 LOAN RECOVERY" REAL DEFAULT 0.00')
    except:
        pass 

    # 2. Update the Math to include the missing column
    cursor.execute('''
        UPDATE master_payroll
        SET "TOTAL DEDUCTION" =
            IFNULL("EMPLOYEE PENSIONS", 0) +
            IFNULL("NHF DED.", 0) +
            IFNULL("PAYE", 0) +
            IFNULL("COOP 1 CONTR/SPEC SAVINGS", 0) +
            IFNULL("COOP. LOAN RECOVERY", 0) +
            IFNULL("COOP 2 CONTR/SPEC SAVINGS", 0) +
            IFNULL("COOP 2 LOAN RECOVERY", 0)
    ''')

    # 3. Recalculate Net Pay
    cursor.execute('''
        UPDATE master_payroll
        SET "NET PAY" = IFNULL("GROSS SALARY", 0) - IFNULL("TOTAL DEDUCTION", 0)
    ''')

    conn.commit()
    conn.close()
    print("✅ PATCH APPLIED! All Net Pays are now mathematically perfect.")

if __name__ == "__main__":
    run_patch()