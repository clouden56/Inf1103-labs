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
    inventory = []
    add_product(inventory, "P001", "Laptop", 1200.00, 15)
    add_product(inventory, "P002", "Mouse", 25.50, 40)
    add_product(inventory, "P003", "Keyboard", 45.00, 25)
    display_all(inventory)

if __name__ == "__main__":
    main()
