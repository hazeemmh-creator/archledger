import pandas as pd
import sqlite3

# 1. Setup the GPS for the Delivery Truck
# Ensure your Excel file is copied directly into your VS Code folder!
excel_file = "NEW UPGRADED PAYROLL SYSTEM APP GMN.xlsm" 
target_sheet = "DB_Master_Payroll"

print("Starting the delivery truck... please wait.")

try:
    # 2. Read the data straight from your Excel sheet
    df = pd.read_excel(excel_file, sheet_name=target_sheet)
    
    # We clean up any empty rows at the bottom of your Excel sheet just in case
    df = df.dropna(how="all") 
    
    print(f"Success! Loaded {len(df)} staff records from Excel.")

    # 3. Open the Vault
    conn = sqlite3.connect("payroll_vault.db")

    # 4. Dump the data into the 'master_payroll' table
    # if_exists="replace" means it will perfectly match your Excel columns automatically!
    df.to_sql("master_payroll", conn, if_exists="replace", index=False)
    
    # Lock the Vault
    conn.close()

    print("Gbosa! All data successfully securely moved to the Payroll Vault!")

except FileNotFoundError:
    print("Wahala: Could not find the Excel file. Are you sure it is inside the folder and the name has the right extension (.xlsx or .xlsm)?")
except Exception as e:
    print(f"Error: {e}")