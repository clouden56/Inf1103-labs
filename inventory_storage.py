import json
import os

from digital_product import DigitalProduct
from inventory import Inventory
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def supplier_to_dict(supplier: Supplier) -> dict[str, str]:
    return {
        "id": supplier.get_supplier_id(),
        "name": supplier.get_name(),
        "contact_email": supplier.get_contact_email(),
    }


def dict_to_supplier(item: dict) -> Supplier:
    return Supplier(item["id"], item["name"], item["contact_email"])


def product_to_dict(product: Product) -> dict[str, str | float | int | None]:
    data: dict[str, str | float | int | None] = {
        "type": None,
        "id": product.get_product_id(),
        "name": product.get_name(),
        "price": product.get_price(),
        "stock": product.get_stock(),
        # Save only the supplier's ID; the supplier itself is saved once in "suppliers"
        "supplier_id": product.get_supplier().get_supplier_id(),
    }
    if isinstance(product, PhysicalProduct):
        data["type"] = "physical"
        data["weight"] = product.get_weight()
    elif isinstance(product, DigitalProduct):
        data["type"] = "digital"
        data["download_size"] = product.get_download_size()
    return data


def dict_to_product(item: dict, supplier: Supplier) -> Product | None:
    # The saved "type" decides which subclass to rebuild
    product_type = item.get("type")
    if product_type == "physical":
        return PhysicalProduct(item["id"], item["name"], item["price"], item["stock"],
                               supplier, item["weight"])
    if product_type == "digital":
        return DigitalProduct(item["id"], item["name"], item["price"], item["stock"],
                              supplier, item["download_size"])
    return None


def load_inventory(file_path: str) -> tuple[Inventory, dict[str, Supplier]]:
    inventory = Inventory()
    suppliers: dict[str, Supplier] = {}
    file_name = os.path.basename(file_path)
    if not os.path.exists(file_path):
        print(f"{file_name} not found. Starting with an empty inventory.")
        return inventory, suppliers
    print(f"{file_name} found.")
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        print("Error: inventory file is corrupted. Starting with an empty inventory.")
        return inventory, suppliers

    # Suppliers are created first so products can be linked to the same Supplier objects
    for item in data.get("suppliers", []):
        supplier = dict_to_supplier(item)
        suppliers[supplier.get_supplier_id()] = supplier

    for item in data.get("products", []):
        supplier = suppliers.get(item.get("supplier_id"))
        if supplier is None:
            print(f"Warning: skipping {item.get('id')} - unknown supplier {item.get('supplier_id')!r}.")
            continue
        product = dict_to_product(item, supplier)
        if product is None:
            print(f"Warning: skipping {item.get('id')} - unknown product type {item.get('type')!r}.")
            continue
        inventory.add_product(product)
    # Replace the "add" entries created above with the saved history
    inventory.load_history(data.get("history", []))
    print("Inventory loaded successfully.")
    return inventory, suppliers


def save_inventory(inventory: Inventory, suppliers: dict[str, Supplier], file_path: str) -> None:
    all_suppliers = dict(suppliers)
    for product in inventory.get_products():
        supplier = product.get_supplier()
        all_suppliers[supplier.get_supplier_id()] = supplier
    data = {
        "suppliers": [supplier_to_dict(supplier) for supplier in all_suppliers.values()],
        "products": [product_to_dict(product) for product in inventory.get_products()],
        "history": inventory.get_history(),
    }
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)
