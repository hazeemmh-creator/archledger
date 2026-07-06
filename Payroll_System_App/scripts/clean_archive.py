import sqlite3

def fix_archive_mixup():
    """
    Deletes any records from 2022 to 2035 that accidentally 
    got saved into the historical_payroll table.
    """
    # Connect to the database we created earlier
    conn = sqlite3.connect('hawea_payroll.db')
    cursor = conn.cursor()
    
    # Execute the deletion command for years 2022 and above
    cursor.execute("DELETE FROM historical_payroll WHERE payroll_year >= 2022")
    
    # Check how many rows were deleted
    deleted_records = cursor.rowcount
    
    # Save the changes
    conn.commit()
    conn.close()
    
    print("🧹 Cleanup Complete, Chief!")
    print(f"Successfully erased {deleted_records} misplaced active records from the Archive.")
    print("The Archive now only holds 2010 to 2021.")

if __name__ == "__main__":
    fix_archive_mixup()