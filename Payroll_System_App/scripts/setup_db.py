import sqlite3

def setup_database():
    """
    Creates the main database and the two foundational tables: 
    active_payroll (for current ops) and historical_payroll (for legacy archives).
    """
    # 1. Connect to the SQLite database 
    # (If 'hawea_payroll.db' doesn't exist, Python will create it for you)
    conn = sqlite3.connect('hawea_payroll.db')
    cursor = conn.cursor()

    # 2. SQL command to create the ACTIVE payroll table
    active_table_sql = """
    CREATE TABLE IF NOT EXISTS active_payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id TEXT NOT NULL,
        staff_name TEXT NOT NULL,
        designation TEXT,
        grade_level TEXT,
        net_salary REAL NOT NULL,
        payroll_month INTEGER NOT NULL,
        payroll_year INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # 3. SQL command to create the HISTORICAL payroll table
    # Notice the extra 'source_file' column for our audit trail
    historical_table_sql = """
    CREATE TABLE IF NOT EXISTS historical_payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id TEXT NOT NULL,
        staff_name TEXT NOT NULL,
        designation TEXT,
        grade_level TEXT,
        net_salary REAL NOT NULL,
        payroll_month INTEGER NOT NULL,
        payroll_year INTEGER NOT NULL,
        source_file TEXT, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    # 4. Execute the SQL commands
    cursor.execute(active_table_sql)
    cursor.execute(historical_table_sql)

    # 5. Save (commit) the changes and close the connection
    conn.commit()
    conn.close()
    
    print("Database setup complete, Chief!")
    print("Tables 'active_payroll' and 'historical_payroll' are ready for action.")

# --- Execute the setup ---
if __name__ == "__main__":
    setup_database()