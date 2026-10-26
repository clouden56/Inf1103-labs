import json
import os

from inventory import Inventory
from product import Product


def load_inventory(file_path):
    inventory = Inventory()
    file_name = os.path.basename(file_path)
    if not os.path.exists(file_path):
        print(f"{file_name} not found. Starting with an empty inventory.")
        return inventory
    print(f"{file_name} found.")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Error: inventory file is corrupted. Starting with an empty inventory.")
        return inventory

    for item in data.get("products", []):
        inventory.add_product(Product(item["id"], item["name"], item["price"], item["stock"]))
    # Replace the "add" entries created above with the saved history
    inventory.load_history(data.get("history", []))
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, file_path):
    products = []
    for product in inventory.get_products():
        products.append({
            "id": product.get_product_id(),
            "name": product.get_name(),
            "price": product.get_price(),
            "stock": product.get_stock(),
        })
    with open(file_path, "w") as file:
        json.dump({"products": products, "history": inventory.get_history()}, file, indent=4)
