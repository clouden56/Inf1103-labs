"""Lab 8 demonstrations: run each 'Predict first' scenario and compare with your prediction."""
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def heading(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def show_product_details(product: Product) -> None:
    # Accepts any Product: works for every subclass without changes (LSP)
    product.display_information()
    print(product.get_fulfilment_info())


def demo_association() -> None:
    heading("2.2 Association: Supplier and Product")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, supplier, 4.2)
    operating_system = DigitalProduct("D100", "Operating System", 139.00, 50, supplier, 5200)
    print(f"Supplier and Product are separate objects: {guitar is not supplier}")

    del supplier
    print("After 'del supplier', each Product still displays its supplier:")
    guitar.get_supplier().display_information()
    operating_system.get_supplier().display_information()
    print(f"Both Products refer to the same Supplier object: "
          f"{guitar.get_supplier() is operating_system.get_supplier()}")


def demo_aggregation() -> None:
    heading("3.2 Aggregation: Inventory and Product")
    supplier = Supplier("S004", "MusicHub Supplies", "hello@musichub.example.com")
    guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, supplier, 4.2)
    print("Product created before any Inventory exists.")

    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(guitar)
    print(f"Added to Inventory A. A finds it: {inventory_a.find_product('P100') is guitar}")

    removed = inventory_a.remove_product("P100")
    print(f"Removed from Inventory A. A finds it: {inventory_a.find_product('P100')}")
    print(f"Removed object is the same Product: {removed is guitar}")
    print("Product still works after removal:")
    guitar.update_stock(8)
    guitar.display_information()

    inventory_b.add_product(guitar)
    print(f"Added the same Product to Inventory B: {inventory_b.find_product('P100') is guitar}")


def demo_composition() -> None:
    heading("4.3 Composition: Order and OrderLine")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    laptop = PhysicalProduct("P001", "Laptop", 1200.00, 15, supplier, 2.0)
    antivirus = DigitalProduct("D001", "Antivirus Software", 49.90, 100, supplier, 350)

    order_1 = Order("O001")
    order_1.add_order_line(laptop, 2)
    order_1.add_order_line(antivirus, 3)
    order_1.display_order()

    order_2 = Order("O002")
    order_2.add_order_line(laptop, 1)
    order_2.display_order()

    line_1 = order_1.get_order_lines()[0]
    line_2 = order_2.get_order_lines()[0]
    print(f"\nLaptop added to two Orders:")
    print(f"  OrderLine objects are different: {line_1 is not line_2} "
          f"(id {id(line_1)} vs {id(line_2)})")
    print(f"  Product objects are the same:    {line_1.get_product() is line_2.get_product()} "
          f"(id {id(line_1.get_product())})")
    print("  => 2 OrderLine objects, 1 Product object")

    order_1.remove_order_line("D001")
    print("\nRemoved the Antivirus line through the Order:")
    order_1.display_order()
    print(f"Antivirus Product still exists: {antivirus.get_name()}")


def demo_lsp() -> None:
    heading("6.2 Substitutability (LSP)")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    products: list[Product] = [
        PhysicalProduct("P006", "Gaming Chair", 150.00, 13, supplier, 18.0),
        DigitalProduct("D001", "Antivirus Software", 49.90, 100, supplier, 350),
    ]
    for product in products:
        show_product_details(product)
        print()

    print("Both subclasses keep Product's update_stock() expectations:")
    for product in products:
        print(f"  {product.get_name()}: update_stock(20) -> {product.update_stock(20)}, "
              f"update_stock(-5) -> {product.update_stock(-5)}, stock = {product.get_stock()}")


def demo_polymorphism() -> None:
    heading("7.2 Polymorphism through the Product collection")
    supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
    inventory = Inventory()
    inventory.add_product(PhysicalProduct("P004", "Monitor", 299.99, 10, supplier, 5.5))
    inventory.add_product(DigitalProduct("0808", "Lab8Product", 8.00, 8, supplier, 8))

    # One loop, no isinstance(): each object supplies its own implementation
    for product in inventory.get_products():
        product.display_information()
        print(product.get_fulfilment_info())
        print()


if __name__ == "__main__":
    demo_association()
    demo_aggregation()
    demo_composition()
    demo_lsp()
    demo_polymorphism()
