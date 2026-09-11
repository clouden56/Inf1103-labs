inventory = 0
failed_entries = 0

while True:
    entry = input("Enter stock quantity or type 'quit': ").strip()

    if entry.lower() == "quit":
        break

    if entry.startswith("-"):
        print("Error: Negative values are not allowed.")
        failed_entries += 1
        continue

    if not entry.isdigit():
        print("Error: Please enter a valid integer.")
        failed_entries += 1
        continue

    quantity = int(entry)
    inventory += quantity

    if inventory > 500:
        print("Alert: Inventory exceeds 500 units.")
        break

print(f"Total Units Processed: {inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")