import sqlite3

def force_mapping():
    conn = sqlite3.connect('payroll_vault.db')
    cursor = conn.cursor()
    
    # Wipe the table to ensure no "lazy" mappings exist
    cursor.execute("DELETE FROM header_mapping")
    
    # The "Universal Mapping" - covers every possible HR variation
    mapping = [
        ("COOP 1", "COOP 1 CONTR/SPEC SAVINGS"),
        ("COOP 1 CONTR/SPEC SAVINGS", "COOP 1 CONTR/SPEC SAVINGS"),
        ("COOPERATIVE 1", "COOP 1 CONTR/SPEC SAVINGS"),
        ("COOP 2", "COOP 2 CONTR/SPEC SAVINGS"),
        ("COOP 2 CONTR/SPEC SAVINGS", "COOP 2 CONTR/SPEC SAVINGS"),
        ("COOPERATIVE 2", "COOP 2 CONTR/SPEC SAVINGS"),
        ("COOP 1 LOAN RECOVERY", "COOP 1 LOAN RECOVERY"),
        ("COOP 2 LOAN RECOVERY", "COOP 2 LOAN RECOVERY")
    ]
    
    cursor.executemany("INSERT INTO header_mapping (messy_header, clean_standard) VALUES (?, ?)", mapping)
    conn.commit()
    conn.close()
    print("✅ Mapping rules enforced.")

force_mapping()