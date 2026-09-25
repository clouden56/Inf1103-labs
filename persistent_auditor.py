import os

INVENTORY_FILE = os.environ.get("INVENTORY_FILE", "inventory.txt")

def load_inventory():
    total = 0
    history = []
    try:
        with open(INVENTORY_FILE, "r") as file:
            for line in file:
                key, _, value = line.strip().partition("=")
                if key == "total" and value:
                    total = int(value)
                elif key == "history" and value:
                    history = [int(amount) for amount in value.split(",")]
    except FileNotFoundError:
        print("No inventory file found. Starting with an empty inventory.")
    return total, history

def get_valid_input():
    entry = input("Enter stock quantity or type 'quit': ").strip()
    if entry.lower() == "quit":
        return "quit"
    if entry.startswith("-"):
        print("Error: Negative values are not allowed.")
        return None
    if not entry.isdigit():
        print("Error: Please enter a valid integer.")
        return None
    return int(entry)

def process_delivery(current_total, new_value):
    return current_total + new_value

def calculate_tax(amount):
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

def main():
    inventory, history = load_inventory()
    failed_entries = 0
    deliveries_processed = 0

    print(f"Current Inventory: {inventory}")
    print(f"Transaction History: {history}")

    while True:
        value = get_valid_input()

        if value == "quit":
            break

        if value is None:
            failed_entries += 1
            continue

        inventory = process_delivery(inventory, value)
        history.append(value)
        tax = calculate_tax(value)
        deliveries_processed += 1

        print(f"Tax for this delivery: {tax}")


        if inventory > 500:
            print("Alert: Inventory exceeds 500 units.")
            break

    generate_report(inventory, failed_entries)
    print(f"Transaction History: {history}")

if __name__ == "__main__":
    main()
