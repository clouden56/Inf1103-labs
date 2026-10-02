import json
import os

INVENTORY_FILE = os.environ.get("INVENTORY_FILE", "inventory.json")

def load_inventory():
    if not os.path.exists(INVENTORY_FILE):
        print(f"{os.path.basename(INVENTORY_FILE)} not found. Starting with an empty inventory.")
        return [], []
    print(f"{os.path.basename(INVENTORY_FILE)} found.")
    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Error: inventory file is corrupted. Starting with an empty inventory.")
        return [], []
    print("Inventory loaded successfully.")
    return data.get("products", []), data.get("history", [])

def add_product(inventory, product_id, name, price, stock):
    if search_product(inventory, product_id) is not None:
        return False
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
    })
    return True

def update_stock(inventory, product_id, new_stock):
    product = search_product(inventory, product_id)
    if product is None:
        return False
    product["stock"] = new_stock
    return True

def search_product(inventory, product_id):
    for product in inventory:
        if product["id"].upper() == product_id.upper():
            return product
    return None

def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("Inventory is empty.")
    for product in inventory:
        print(f"ID: {product['id']} | Name: {product['name']} | "
              f"Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 48)

def main():
    inventory, history = load_inventory()
    display_all(inventory)
    print(f"Transaction History: {history}")

if __name__ == "__main__":
    main()
