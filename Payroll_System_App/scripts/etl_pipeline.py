import csv
import hashlib

def generate_staff_id(name):
    """
    Creates a unique, consistent ID based on the staff name.
    It creates a digital fingerprint so the same name always gets the same ID.
    """
    # We clean the name, make it lowercase, and generate a 6-character code
    fingerprint = hashlib.md5(name.strip().lower().encode()).hexdigest()[:6].upper()
    return f"STF-{fingerprint}"

def clean_payroll_data(file_path):
    """
    Extracts and transforms the messy CSV into clean database-ready records.
    """
    clean_records = []
    
    # Open and read the CSV file
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        
        for row in reader:
            # Skip empty rows or rows that don't have enough columns
            if not row or len(row) < 20:
                continue
                
            staff_name = row[0].strip()
            
            # Make sure it's a real name and not a header or department title
            ignore_list = ["STAFF NAME", "DG OFFICE", "LEG. SUPPORT SEVICES", ""]
            if staff_name not in ignore_list:
                try:
                    designation = row[3].strip()
                    
                    # The Net Salary is at the very end of your CSV rows. 
                    # We grab the last column, remove any commas, and turn it into a decimal number (float).
                    net_salary_str = row[-1].replace(',', '').strip()
                    net_salary = float(net_salary_str)
                    
                    # Generate the unique ID
                    staff_id = generate_staff_id(staff_name)
                    
                    # Save the clean record
                    clean_records.append({
                        "Staff ID": staff_id,
                        "Name": staff_name,
                        "Designation": designation,
                        "Net Salary": net_salary
                    })
                except ValueError:
                    # If the script can't turn the salary into a number, it's a title row. Skip it.
                    continue
                    
    return clean_records

# --- Run the Test ---
if __name__ == "__main__":
    # Make sure this matches your file name exactly
    csv_file_name = "2012 salary data sheet.xlsx - May 2012.csv"
    
    print("Oga, starting data extraction...\n")
    records = clean_payroll_data(csv_file_name)
    
    print(f"Successfully extracted {len(records)} staff records!\n")
    print("Here is a clean preview of the first 5 records:")
    print("-" * 50)
    
    for i in range(min(5, len(records))):
        print(f"ID: {records[i]['Staff ID']} | Name: {records[i]['Name']} | Role: {records[i]['Designation']} | Net: N{records[i]['Net Salary']:,.2f}")