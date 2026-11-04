import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct


def product_to_dict(product):
    data = {
        "type": None,
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock(),
    }
    if isinstance(product, PhysicalProduct):
        data["type"] = "physical"
        data["weight"] = product.get_weight()
    elif isinstance(product, DigitalProduct):
        data["type"] = "digital"
        data["download_size"] = product.get_download_size()
    return data


def dict_to_product(item):
    # The saved "type" decides which subclass to rebuild
    product_type = item.get("type")
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"], item["stock"], item["weight"])
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"], item["stock"], item["download_size"])
    return None


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
        product = dict_to_product(item)
        if product is None:
            print(f"Warning: skipping {item.get('id')} - unknown product type {item.get('type')!r}.")
            continue
        inventory.add_product(product)
    # Replace the "add" entries created above with the saved history
    inventory.load_history(data.get("history", []))
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, file_path):
    products = [product_to_dict(product) for product in inventory.get_products()]
    with open(file_path, "w") as file:
        json.dump({"products": products, "history": inventory.get_history()}, file, indent=4)
