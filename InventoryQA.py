from InventoryManagement import InventoryManagement

def run_tests():
    manager = InventoryManagement()
    
    # Setup Default Input Data
    manager.add_product("Warehouse A", "P101", "Laptop", 10, threshold=3)
    manager.add_product("Warehouse B", "P101", "Laptop", 2, threshold=3)
    manager.add_product("Warehouse C", "P102", "Phone", 15, threshold=5)
    manager.manage_supplier("P101", "TechSupplier Inc")

    # 1. Stock Availability Test
    wh = manager.select_warehouse_for_fulfillment("P101", 4)
    print("Stock Availability Test Passed:", wh == "Warehouse A")

    # 2. Insufficient Inventory Test
    wh_fail = manager.select_warehouse_for_fulfillment("P101", 20)
    print("Insufficient Inventory Test Passed:", wh_fail is None)

    # 3. Warehouse Transfer Test
    manager.transfer_stock("Warehouse A", "Warehouse B", "P101", 3)
    print("Warehouse Transfer Test Passed:", manager.warehouses["Warehouse B"]["P101"]["qty"] == 5)

    # 4. Concurrent Orders Simulation Test
    order1 = manager.select_warehouse_for_fulfillment("P101", 2)
    if order1:
        manager.remove_product(order1, "P101", 2)
    order2 = manager.select_warehouse_for_fulfillment("P101", 2)
    print("Concurrent Orders Test Passed:", order2 == "Warehouse A" or order2 == "Warehouse B")

    # 5. Reorder Threshold & Low-stock Detection Test
    low_stock = manager.detect_low_stock()
    print("Reorder Threshold Test Passed:", len(low_stock) > 0)

    # 6. Invalid Product Test
    invalid_rem = manager.remove_product("Warehouse A", "P999", 5)
    print("Invalid Product Test Passed:", not invalid_rem)

    # 7. Negative Inventory Test
    neg_add = manager.add_product("Warehouse A", "P103", "Tablet", -5)
    print("Negative Inventory Test Passed:", not neg_add)

    # 8. Multiple Warehouses Verification
    print("Multiple Warehouses Test Passed:", set(manager.warehouses.keys()) == {"Warehouse A", "Warehouse B", "Warehouse C"})

if __name__ == "__main__":
    run_tests()
