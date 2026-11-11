import os

from digital_product import DigitalProduct
from inventory import Inventory
from inventory_storage import load_inventory, save_inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier

INVENTORY_FILE: str = os.environ.get("INVENTORY_FILE", "inventory.json")

def get_non_negative_int(prompt: str) -> int | None:
    entry = input(prompt).strip()
    if not entry.isdigit():
        print("Error: Please enter a whole number that is 0 or more.")
        return None
    return int(entry)

def get_non_negative_float(prompt: str, label: str = "Price") -> float | None:
    entry = input(prompt).strip()
    try:
        value = float(entry)
    except ValueError:
        print(f"Error: Please enter a valid {label.lower()}.")
        return None
    if value < 0:
        print(f"Error: {label} cannot be negative.")
        return None
    return value

def get_product_type() -> str | None:
    entry = input("Product Type (1 = Physical, 2 = Digital): ").strip()
    if entry == "1":
        return "physical"
    if entry == "2":
        return "digital"
    print("Error: Please enter 1 for Physical or 2 for Digital.")
    return None

def choose_supplier(suppliers: dict[str, Supplier]) -> Supplier | None:
    if suppliers:
        print("Available suppliers: " + ", ".join(
            f"{supplier.get_supplier_id()} ({supplier.get_name()})" for supplier in suppliers.values()))
    supplier_id = input("Supplier ID: ").strip().upper()
    if not supplier_id:
        print("Error: Supplier ID cannot be empty.")
        return None
    if supplier_id in suppliers:
        return suppliers[supplier_id]

    # The Supplier is created independently, then given to the Product (association)
    print(f"Supplier {supplier_id} not found. Creating a new supplier.")
    name = input("Supplier Name: ").strip()
    if not name:
        print("Error: Supplier name cannot be empty.")
        return None
    contact_email = input("Supplier Contact Email: ").strip()
    if "@" not in contact_email:
        print("Error: Please enter a valid email address.")
        return None
    supplier = Supplier(supplier_id, name, contact_email)
    suppliers[supplier_id] = supplier
    return supplier

def handle_add(inventory: Inventory, suppliers: dict[str, Supplier]) -> None:
    print("\nAdd New Product")
    product_type = get_product_type()
    if product_type is None:
        return
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Error: Product ID cannot be empty.")
        return
    if inventory.find_product(product_id) is not None:
        print(f"Error: Product {product_id} already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Error: Product name cannot be empty.")
        return
    price = get_non_negative_float("Price: ")
    if price is None:
        return
    stock = get_non_negative_int("Stock Quantity: ")
    if stock is None:
        return
    supplier = choose_supplier(suppliers)
    if supplier is None:
        return
    product: Product
    if product_type == "physical":
        weight = get_non_negative_float("Weight (kg): ", "Weight")
        if weight is None:
            return
        product = PhysicalProduct(product_id, name, price, stock, supplier, weight)
    else:
        download_size = get_non_negative_float("Download Size (MB): ", "Download size")
        if download_size is None:
            return
        product = DigitalProduct(product_id, name, price, stock, supplier, download_size)
    inventory.add_product(product)
    print("\nProduct added successfully!")

def handle_update(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")
    new_stock = get_non_negative_int("\nNew Stock Quantity: ")
    if new_stock is None:
        return
    inventory.update_stock(product.get_product_id(), new_stock)
    print("\nStock updated successfully!")

def handle_search(inventory: Inventory) -> None:
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print("-" * 48)
    # Works the same for any Product subclass (polymorphism)
    product.display_information()
    print(f"Fulfilment: {product.get_fulfilment_info()}")
    product.get_supplier().display_information()
    print("-" * 48)

def handle_remove(inventory: Inventory) -> None:
    print("\nRemove Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.remove_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print(f"\n{product.get_name()} ({product.get_product_id()}) removed from inventory.")

def handle_order(inventory: Inventory) -> None:
    print("\nCreate Order")
    order_id = input("Order ID: ").strip().upper()
    if not order_id:
        print("Error: Order ID cannot be empty.")
        return
    order = Order(order_id)
    while True:
        product_id = input("\nProduct ID to add (press Enter to finish): ").strip()
        if not product_id:
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_non_negative_int(f"Quantity of {product.get_name()}: ")
        if quantity is None:
            continue
        if quantity == 0 or quantity > product.get_stock():
            print(f"Error: Quantity must be between 1 and {product.get_stock()} (current stock).")
            continue
        order.add_order_line(product, quantity)
        print(f"Added {quantity} x {product.get_name()} to order {order_id}.")
    order.display_order()

def show_menu() -> None:
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Remove Product")
    print("6. Create Order")
    print("7. Save Inventory")
    print("8. Exit")
    print("----------------------------")

def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()
    inventory, suppliers = load_inventory(INVENTORY_FILE)
    show_menu()

    while True:
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            handle_add(inventory, suppliers)
        elif option == "3":
            handle_update(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            handle_remove(inventory)
        elif option == "6":
            handle_order(inventory)
        elif option == "7":
            print("\nSaving inventory...")
            save_inventory(inventory, suppliers, INVENTORY_FILE)
            print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}.")
        elif option == "8":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, suppliers, INVENTORY_FILE)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 8.")
            show_menu()

if __name__ == "__main__":
    main()
