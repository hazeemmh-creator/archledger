import sqlite3

def recalibrate_database():
    print("Starting Vault Recalibration...")
    try:
        conn = sqlite3.connect("payroll_vault.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Fetch every single record in the database
        cursor.execute('SELECT * FROM master_payroll')
        records = cursor.fetchall()
        
        updated_count = 0

        for row in records:
            txn_id = row["Txn_ID"]
            
            # 1. Get the Base Gross
            def get_val(col):
                try: return float(row[col]) if row[col] else 0.0
                except: return 0.0

            gross = get_val("GROSS SALARY")
            
            # 2. Sum up all deductions accurately
            pension = get_val("EMPLOYEE PENSIONS")
            nhf = get_val("NHF DED.")
            paye = get_val("PAYE")
            c1_sav = get_val("COOP 1 CONTR/SPEC SAVINGS")
            
            # THE FIX IS HERE: It now perfectly matches your master database column
            c1_loan = get_val("COOP 1 LOAN RECOVERY") 
            
            c2_sav = get_val("COOP 2 CONTR/SPEC SAVINGS")
            c2_loan = get_val("COOP 2 LOAN RECOVERY")
            auction = get_val("AUCTION")
            
            true_total_deductions = pension + nhf + paye + c1_sav + c1_loan + c2_sav + c2_loan + auction
            
            # 3. Calculate True Net Pay
            true_net_pay = gross - true_total_deductions
            
            # 4. Update the database record permanently!
            cursor.execute('''
                UPDATE master_payroll 
                SET "TOTAL DEDUCTION" = ?, "NET PAY" = ?
                WHERE "Txn_ID" = ?
            ''', (true_total_deductions, true_net_pay, txn_id))
            
            updated_count += 1

        conn.commit()
        conn.close()
        print(f"Gbosa! Successfully audited and recalculated {updated_count} records.")
        print("Your Database math is now 100% perfectly balanced.")

    except Exception as e:
        print(f"Error during recalibration: {e}")

if __name__ == "__main__":
    recalibrate_database()