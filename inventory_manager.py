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

def save_inventory(inventory, history):
    with open(INVENTORY_FILE, "w") as file:
        json.dump({"products": inventory, "history": history}, file, indent=4)

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

def record_transaction(history, product_id, action, amount):
    history.append({"id": product_id, "action": action, "amount": amount})

def handle_add(inventory, history):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Error: Product ID cannot be empty.")
        return
    if search_product(inventory, product_id) is not None:
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
    add_product(inventory, product_id, name, price, stock)
    record_transaction(history, product_id, "add", stock)
    print("\nProduct added successfully!")

def handle_update(inventory, history):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found:")
    print(f"Name: {product['name']}")
    print(f"Current Stock: {product['stock']}")
    new_stock = get_non_negative_int("\nNew Stock Quantity: ")
    if new_stock is None:
        return
    change = new_stock - product["stock"]
    update_stock(inventory, product["id"], new_stock)
    record_transaction(history, product["id"], "update", change)
    print("\nStock updated successfully!")

def handle_search(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = search_product(inventory, product_id)
    if product is None:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
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
    inventory, history = load_inventory()
    show_menu()

    while True:
        option = input("\nEnter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            handle_add(inventory, history)
        elif option == "3":
            handle_update(inventory, history)
        elif option == "4":
            handle_search(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory, history)
            print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory, history)
            print("Inventory saved successfully.")
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please enter a number from 1 to 6.")
            show_menu()

if __name__ == "__main__":
    main()
