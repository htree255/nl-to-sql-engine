import sqlite3
import os

def create_sample_database():
    """
    This function build a sample database.
    Tables: employees, sales, and products.
    """
    #Create database file
    #If database exists, just open it
    db_path = "company.db"
    connection = sqlite3.connect(db_path)

    #cursor is like a workspace
    cursor = connection.cursor()

    # --- Create the employees table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id      INTEGER PRIMARY KEY,
            name    TEXT,
            dept    TEXT,
            salary  INTEGER
        )
    """)

 # --- Create the products table ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id      INTEGER PRIMARY KEY,
            name    TEXT,
            price   REAL,
            stock   INTEGER
        )
    """)

    # --- Create the sales table ---
    # Note: employee_id and product_id are "foreign keys"
    # They connect this table back to the other two
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id          INTEGER PRIMARY KEY,
            employee_id INTEGER,
            product_id  INTEGER,
            quantity    INTEGER,
            sale_date   TEXT
        )
    """)

    # --- Fill in some sample rows ---
    cursor.executemany("INSERT OR IGNORE INTO employees VALUES (?,?,?,?)", [
        (1, "Alice",   "Engineering", 95000),
        (2, "Bob",     "Sales",       72000),
        (3, "Carol",   "Sales",       68000),
        (4, "David",   "Engineering", 88000),
        (5, "Eve",     "Marketing",   74000),
    ])

    cursor.executemany("INSERT OR IGNORE INTO products VALUES (?,?,?,?)", [
        (1, "Laptop",  999.99, 50),
        (2, "Monitor", 349.99, 120),
        (3, "Keyboard", 79.99, 300),
        (4, "Mouse",    49.99, 400),
    ])

    cursor.executemany("INSERT OR IGNORE INTO sales VALUES (?,?,?,?,?)", [
        (1,  2, 1, 3, "2024-01-15"),
        (2,  3, 2, 5, "2024-01-18"),
        (3,  2, 3, 10, "2024-02-02"),
        (4,  3, 1, 2, "2024-02-14"),
        (5,  2, 4, 8, "2024-03-01"),
        (6,  3, 2, 3, "2024-03-10"),
        (7,  2, 1, 1, "2024-03-22"),
        (8,  3, 3, 6, "2024-04-05"),
    ])

    # Save everything to disk
    connection.commit()
    print("Database created at: ")
    return connection


def run_query(connection, sql):
    """
    Runs a SQL query and prints the results
    """

    cursor = connection.cursor()

    try:

        cursor.execute(sql)
        rows = cursor.fetchall()
 
        return {"success": True, "rows": rows}

    except sqlite3.Error as e:
        return {"success": False, "error": str(e)}

def print_result(result):
    """
    Print a result dictionary from run_query in a readable way.
    Separated from run_query so the validation loop can check
    success/failure before deciding whether to display anything.
    """

    if not result["success"]:
        print (f"SQL Error: {result["error"]}")
        return
    
    rows = result["rows"]
    #columns = result["columns"]

    if not rows:
        print("(query ran successfully, but returned no rows)")
        return
    
    #print(" | ".join(columns))
    print("-" * 40)
    for row in rows:
        print(" | ".join(str(val) for val in row))



if __name__ == "__main__":
    conn = create_sample_database()

    print("\n--- All employees ---")
    run_query(conn, "SELECT * FROM employees")

    print("\n--- Products under $100 ---")
    run_query(conn, "SELECT name, price FROM products WHERE price < 100")

    print("\n--- My own query ---")
    run_query(conn, "SELECT name, salary FROM employees WHERE dept = 'Engineering'")









