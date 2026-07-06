import pandas as pd
import os
import glob

print("Starting the Smart Data Medic Engine...\n")

# 1. RADAR: Find ALL excel files in the folder (both .xlsx and .xls)
excel_files = glob.glob("*.xls*")

if not excel_files:
    print("❌ No Excel files found in this folder at all, Oga!")

for file in excel_files:
    # 2. Skip files we already cleaned so we don't clean them twice
    if "_CLEANED" in file:
        continue
        
    print(f"⚙️ Processing: {file}...")
    try:
        # Load the raw file
        df = pd.read_excel(file)
        
        # Drop completely empty rows and ruthlessly destroy duplicates
        df_cleaned = df.dropna(how='all').drop_duplicates()
        
        # Save the clean version safely
        base_name, ext = os.path.splitext(file)
        new_name = f"{base_name}_CLEANED.xlsx"
        
        df_cleaned.to_excel(new_name, index=False)
        print(f"  ✅ Success! Saved as: {new_name}\n")
        
    except Exception as e:
        print(f"  ❌ Error reading {file}: {e}\n")

print("Gbosa! All found files cleaned. The Vault is ready for upload.")