import os

from inventory_storage import load_inventory, save_inventory
from product import Product

INVENTORY_FILE = os.environ.get("INVENTORY_FILE", "inventory.json")

def get_non_negative_int(prompt):
    entry = input(prompt).strip()
    if not entry.isdigit():
        print("Error: Please enter a whole number that is 0 or more.")
        return None
    return int(entry)

def get_non_negative_float(prompt):
    entry = input(prompt).strip()
    try:
        value = float(entry)
    except ValueError:
        print("Error: Please enter a valid price.")
        return None
    if value < 0:
        print("Error: Price cannot be negative.")
        return None
    return value

def handle_add(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Error: Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
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
    inventory.add_product(Product(product_id, name, price, stock))
    print("\nProduct added successfully!")

def handle_update(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
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

def handle_search(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.search_product(product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print("-" * 48)
    product.display_information()
    print("-" * 48)

def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")

def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()
    inventory = load_inventory(INVENTORY_FILE)
    show_menu()

    while True:
        option = input("\nEnter option: ").strip()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            handle_add(inventory)
        elif option == "3":
            handle_update(inventory)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory, INVENTORY_FILE)
            print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, INVENTORY_FILE)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
            show_menu()

if __name__ == "__main__":
    main()
