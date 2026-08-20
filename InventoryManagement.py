class InventoryManagement:
    def __init__(self):
        self.warehouses = {"Warehouse A": {}, "Warehouse B": {}, "Warehouse C": {}}
        self.reorder_thresholds = {}
        self.suppliers = {}

    def add_product(self, warehouse, product_id, name, qty, threshold=5):
        if warehouse not in self.warehouses:
            return False
        if qty < 0:
            return False
        self.warehouses[warehouse][product_id] = {
            "name": name,
            "qty": qty
        }
        self.reorder_thresholds[product_id] = threshold
        return True

    def remove_product(self, warehouse, product_id, qty):
        if warehouse not in self.warehouses:
            return False
        if product_id not in self.warehouses[warehouse]:
            return False
        if qty < 0:
            return False
        if self.warehouses[warehouse][product_id]["qty"] < qty:
            return False
        
        self.warehouses[warehouse][product_id]["qty"] -= qty
        return True

    def transfer_stock(self, from_wh, to_wh, product_id, qty):
        if from_wh not in self.warehouses or to_wh not in self.warehouses:
            return False
        if product_id not in self.warehouses[from_wh]:
            return False
        if self.warehouses[from_wh][product_id]["qty"] < qty or qty < 0:
            return False

        prod_name = self.warehouses[from_wh][product_id]["name"]
        success = self.remove_product(from_wh, product_id, qty)
        if not success:
            return False

        if product_id not in self.warehouses[to_wh]:
            threshold = self.reorder_thresholds.get(product_id, 5)
            self.add_product(to_wh, product_id, prod_name, 0, threshold)

        self.warehouses[to_wh][product_id]["qty"] += qty
        return True

    def select_warehouse_for_fulfillment(self, product_id, required_qty):
        for wh in ["Warehouse A", "Warehouse B", "Warehouse C"]:
            if product_id in self.warehouses[wh]:
                if self.warehouses[wh][product_id]["qty"] >= required_qty:
                    return wh
        return None

    def detect_low_stock(self):
        low_stock_items = []
        for wh, inventory in self.warehouses.items():
            for pid, data in inventory.items():
                threshold = self.reorder_thresholds.get(pid, 5)
                if data["qty"] <= threshold:
                    low_stock_items.append((wh, pid, data["qty"]))
        return low_stock_items

    def reorder_item(self, warehouse, product_id, qty):
        if warehouse not in self.warehouses or qty < 0:
            return False
        if product_id not in self.warehouses[warehouse]:
            return False
        self.warehouses[warehouse][product_id]["qty"] += qty
        return True

    def manage_supplier(self, product_id, supplier_name):
        self.suppliers[product_id] = supplier_name
        return True
