import sqlite3

DB_NAME = 'inventory.db'

def init_db():
    # (Connect to the database and create the warehouses table if it doesn't exist)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Create warehouses Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS warehouses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
                   """)
    
    # 2. Create Inventory Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   warehouse_id INTEGER NOT NULL,
                   item_name TEXT NOT NULL,
                   quantity INTEGER NOT NULL,
                   safety_threshold INTEGER DEFAULT 10,
                     FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
                     )
                     """)

    # Clear existing tables to ensure clean data on rerun
    cursor.execute("DELETE FROM inventory")
    cursor.execute("DELETE FROM warehouses")

    #  4. Insert Mock Warehouses (Represneting our 5 nodes )
    warehouses_data = [
        ("Central Hub", "Ibadan"),
        ("North Warehouse", "Kano"),
        ("South Depot", "Lagos"),
        ("East Branch", "Port Harcourt"),
        ("West Storage", "Abeokuta")
    ]
    cursor.executemany("INSERT INTO warehouses (name, location) VALUES (?, ?)", warehouses_data)

    # 5. Insert Mock Inventory Items
    # Note: Some items are deliberately set below the safety_threshold (10)
    inventory_data = [
        (1, "Sugar Bags", 150, 20),                 # Safe
        (1, "Packaging Film", 8, 15),               # LOW STOCK! (8 < 15)
        (2, "Refined Sugar Bags", 200, 30),         # Safe
        (3, "Pumping Valves", 3, 10),               # LOW STOCK! (3 < 10)
        (4, "Filter Cartridges", 25, 10),           #Safe
        (5, "Conveyor Belts", 2, 5)                 # LOW STOCK! (2 < 5)
    ]

    cursor.executemany("""
        INSERT INTO inventory (warehouse_id, item_name, quantity, safety_threshold)
        VALUES (?, ?, ?, ?)
""", inventory_data)
    
    # Save changes and close the connection
    conn.commit()
    conn.close()
    print("Database initialized with 5 warehouse nodes and sample inventory data successfully")

if __name__ == "__main__":
    init_db();