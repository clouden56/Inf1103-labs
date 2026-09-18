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
    inventory = 0
    failed_entries = 0
    deliveries_processed = 0
    
    while True:
        value = get_valid_input()
        
        if value == "quit":
            break
        
        if value is None:
            failed_entries += 1
            continue
            
        inventory = process_delivery(inventory, value)
        tax = calculate_tax(value)
        deliveries_processed += 1
        
        print(f"Tax for this delivery: {tax}")
        
        # From previous lab, though not explicitly required here, retaining it is safe
        if inventory > 500:
            print("Alert: Inventory exceeds 500 units.")
            break
            
    generate_report(inventory, failed_entries)

if __name__ == "__main__":
    main()