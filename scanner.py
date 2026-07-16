import sqlite3

DB_NAME = 'inventory.db'

def check_low_stock_items():

    # 1. Connect to the SQLite database
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 2. SQL query with a JOIN to pull the warehouse name along with the item info
    # To select; Warehouse Name, Item Name, Current Quantity, and Safety Threshold
    # Query to find items below their safety threshold
    query = """
        SELECT i.item_name, i.quantity, i.safety_threshold, w.name AS warehouse_name
        FROM inventory i
        JOIN warehouses w ON i.warehouse_id = w.id
        WHERE i.quantity < i.safety_threshold
    """
    cursor.execute(query)
    low_stock_items = cursor.fetchall()
    
    # 3. Process and display the results
    print("=== STARTING INVENTORY SCAN===")

    if not low_stock_items:
        print("All warehouse nodes are fully stocked! No alerts triggered.")
    else:
        print(f"Alert! Found {len(low_stock_items)} item(s) below safety thresholdS:\n")

        # To loop through te low stock items and display them in a readable format
        for row in low_stock_items:
            item_name, quantity, safety_threshold, warehouse_name = row
            print(f"Warehouse: {warehouse_name} | Item: {item_name} | Current Quantity: {quantity} | Safety Threshold: {safety_threshold}")
            warehouse_name = row[3]
            item_name = row[0]
            quantity = row[1]
            safety_threshold = row[2]

            print(f"⚠️ [ALERT] Warehouse: {warehouse_name}")
            print(f"   - Item: {item_name}")
            print(f"   - Current Stock: {quantity}")
            print(f"   - Safety Threshold: {safety_threshold}")
            print("-" * 40)


    # 4. Close the database connection
    conn.close()
    print("=== INVENTORY SCAN COMPLETED ===")

    # Return the list so we can pass it to our email alerter in the next step
    return low_stock_items
if __name__ == "__main__":
    check_low_stock_items();