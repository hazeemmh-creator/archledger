import sqlite3
import shutil
import os

def run_medic():
    db_file = "payroll_vault.db"
    backup_file = "payroll_vault_BACKUP.db"

    print("🚀 Initiating Data Medic Protocol...")

    # 1. CREATE A SAFETY BACKUP
    if os.path.exists(db_file):
        shutil.copyfile(db_file, backup_file)
        print(f"✅ SAFETY FIRST: Database backed up to '{backup_file}'")
    else:
        print("❌ ERROR: payroll_vault.db not found! Are you in the right folder?")
        return

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 2. FORCE MATHEMATICAL RECONCILIATION
    print("⏳ Running reconciliation on historical records to fix Net Pay bug...")

    # Ensure the COOP 2 column exists just in case it's completely missing from old months
    try:
        cursor.execute('ALTER TABLE master_payroll ADD COLUMN "COOP 2 CONTR/SPEC SAVINGS" REAL DEFAULT 0.00')
    except:
        pass # Column already exists, no wahala!

    # FIXED: Added missing deductions and used the corrected 'COOP 1 LOAN RECOVERY' standard
    cursor.execute('''
        UPDATE master_payroll
        SET "TOTAL DEDUCTION" = 
            IFNULL("EMPLOYEE PENSIONS", 0) +
            IFNULL("NHF DED.", 0) +
            IFNULL("PAYE", 0) +
            IFNULL("COOP 1 CONTR/SPEC SAVINGS", 0) +
            IFNULL("COOP 1 LOAN RECOVERY", 0) + 
            IFNULL("COOP 2 CONTR/SPEC SAVINGS", 0) +
            IFNULL("COOP 2 LOAN RECOVERY", 0) +
            IFNULL("AUCTION", 0)
    ''')

    # Recalculate Net Pay accurately (Gross - Deductions)
    cursor.execute('''
        UPDATE master_payroll
        SET "NET PAY" = IFNULL("GROSS SALARY", 0) - IFNULL("TOTAL DEDUCTION", 0)
    ''')

    # 3. CONSTRUCT THE GLOBAL STAFF DIRECTORY
    print("⏳ Constructing the Global Staff Profiles Vault...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tbl_Staff_Profiles (
            Staff_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            "STAFF NAME" TEXT UNIQUE,
            "DESIGNATION" TEXT,
            "GRADE LEVEL" TEXT,
            "BANK" TEXT DEFAULT '',
            "ACCT NO" TEXT DEFAULT '',
            "PFA" TEXT DEFAULT '',
            "PENSION NO" TEXT DEFAULT '',
            "EMAIL" TEXT DEFAULT ''
        )
    ''')

    # 4. MIGRATE UNIQUE STAFF
    cursor.execute('''
        SELECT DISTINCT "STAFF NAME", "DESIGNATION", "GRADE LEVEL"
        FROM master_payroll
        WHERE "STAFF NAME" IS NOT NULL AND "STAFF NAME" != ''
    ''')
    staff_list = cursor.fetchall()

    count = 0
    for staff in staff_list:
        try:
            cursor.execute('''
                INSERT INTO tbl_Staff_Profiles ("STAFF NAME", "DESIGNATION", "GRADE LEVEL")
                VALUES (?, ?, ?)
            ''', (staff[0], staff[1], staff[2]))
            count += 1
        except sqlite3.IntegrityError:
            # Staff already exists in the profile table, skip quietly
            pass

    conn.commit()
    conn.close()

    print(f"✅ DIRECTORY BUILT: Successfully extracted {count} unique staff profiles.")
    print("✅ MATH CORRECTED: All historical Deductions and Net Pays have been mathematically reconciled.")
    print("🎯 PHASE 1 COMPLETE! The Vault is secure.")

if __name__ == "__main__":
    run_medic()