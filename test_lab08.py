import inspect
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from digital_product import DigitalProduct
from inventory import Inventory
from inventory_storage import load_inventory, save_inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def show_product_details(product: Product) -> str:
    """Uses only behaviour every Product supports (LSP); returns what was printed."""
    output = io.StringIO()
    with redirect_stdout(output):
        product.display_information()
        print(product.get_fulfilment_info())
    return output.getvalue()


class TestAssociation(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
        self.guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, self.supplier, 4.2)
        self.os = DigitalProduct("D100", "Operating System", 139.00, 50, self.supplier, 5200)

    def test_product_stores_reference_to_its_supplier(self):
        self.assertIs(self.guitar.get_supplier(), self.supplier)
        self.assertIs(self.os.get_supplier(), self.supplier)
        self.assertEqual(self.guitar.get_supplier().get_contact_email(), "sales@techsource.example.com")

    def test_supplier_and_products_are_separate_and_independent(self):
        self.assertIsNot(self.guitar, self.supplier)
        supplier = self.supplier
        del self.supplier, supplier  # the Products still hold their own reference
        self.assertEqual(self.guitar.get_supplier().get_name(), "TechSource Pte Ltd")
        # A Supplier can also exist without any Product
        lone_supplier = Supplier("S999", "New Co", "hi@newco.example.com")
        self.assertEqual(lone_supplier.get_name(), "New Co")


class TestAggregation(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
        # Product created before any Inventory exists
        self.guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, self.supplier, 4.2)

    def test_product_can_move_between_inventories_without_being_destroyed(self):
        inventory_a, inventory_b = Inventory(), Inventory()
        inventory_a.add_product(self.guitar)
        removed = inventory_a.remove_product("P100")
        self.assertIs(removed, self.guitar)
        self.assertIsNone(inventory_a.find_product("P100"))
        self.assertTrue(self.guitar.update_stock(7))  # still usable after removal
        inventory_b.add_product(self.guitar)
        self.assertIs(inventory_b.find_product("p100"), self.guitar)

    def test_emptying_inventory_does_not_destroy_products(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.remove_product("P100")
        self.assertEqual(inventory.get_products(), [])
        self.assertEqual(self.guitar.get_name(), "Guitar")

    def test_remove_and_find_missing_product_return_none(self):
        inventory = Inventory()
        self.assertIsNone(inventory.remove_product("P999"))
        self.assertIsNone(inventory.find_product("P999"))


class TestComposition(unittest.TestCase):

    def setUp(self):
        supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
        self.guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, supplier, 4.2)
        self.os = DigitalProduct("D100", "Operating System", 139.00, 50, supplier, 5200)

    def test_order_creates_its_own_order_lines_and_calculates_total(self):
        order = Order("O001")
        order.add_order_line(self.guitar, 2)
        order.add_order_line(self.os, 3)
        lines = order.get_order_lines()
        self.assertEqual(len(lines), 2)
        self.assertTrue(all(isinstance(line, OrderLine) for line in lines))
        self.assertEqual(lines[0].calculate_subtotal(), 700.00)
        self.assertEqual(order.calculate_total(), 700.00 + 417.00)

    def test_same_product_in_two_orders_gives_two_lines_but_one_product(self):
        order_1, order_2 = Order("O001"), Order("O002")
        order_1.add_order_line(self.guitar, 1)
        order_2.add_order_line(self.guitar, 4)
        line_1, line_2 = order_1.get_order_lines()[0], order_2.get_order_lines()[0]
        self.assertIsNot(line_1, line_2)  # each Order owns its own OrderLine
        self.assertIs(line_1.get_product(), line_2.get_product())  # both refer to one Product

    def test_order_line_refers_to_product_but_does_not_own_it(self):
        order = Order("O001")
        order.add_order_line(self.guitar, 1)
        order.remove_order_line("P100")
        self.assertEqual(order.get_order_lines(), ())
        self.assertEqual(self.guitar.get_name(), "Guitar")  # Product unaffected

    def test_order_lines_cannot_be_changed_from_outside(self):
        order = Order("O001")
        order.add_order_line(self.guitar, 1)
        lines = order.get_order_lines()
        self.assertIsInstance(lines, tuple)
        with self.assertRaises(AttributeError):
            lines.append(None)  # a tuple cannot be appended to, so the Order keeps control
        self.assertEqual(len(order.get_order_lines()), 1)


class TestTypeHints(unittest.TestCase):

    def test_type_hints_match_the_design(self):
        hints = inspect.get_annotations
        self.assertIs(hints(Product.__init__)["supplier"], Supplier)
        self.assertEqual(hints(Product.get_supplier)["return"], Supplier)
        self.assertEqual(hints(Inventory.add_product)["product"], Product)
        self.assertEqual(hints(Inventory.find_product)["return"], Product | None)
        self.assertEqual(hints(Inventory.remove_product)["return"], Product | None)
        self.assertEqual(hints(Inventory.get_products)["return"], list[Product])
        self.assertEqual(hints(OrderLine.__init__)["product"], Product)
        self.assertIs(hints(OrderLine.__init__)["quantity"], int)
        self.assertIs(hints(OrderLine.calculate_subtotal)["return"], float)
        self.assertIs(hints(Order.add_order_line)["return"], None)
        self.assertIs(hints(Order.calculate_total)["return"], float)


class TestLiskovAndPolymorphism(unittest.TestCase):

    def setUp(self):
        supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
        self.guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, supplier, 4.2)
        self.os = DigitalProduct("D100", "Operating System", 139.00, 50, supplier, 5200)

    def test_show_product_details_works_for_both_subclasses(self):
        self.assertIn("Weight: 4.20 kg", show_product_details(self.guitar))
        self.assertIn("physical shipping", show_product_details(self.guitar))
        self.assertIn("Download Size: 5200.00 MB", show_product_details(self.os))
        self.assertIn("delivered digitally", show_product_details(self.os))

    def test_both_subclasses_preserve_update_stock_expectations(self):
        for product in (self.guitar, self.os):
            self.assertTrue(product.update_stock(0))
            self.assertTrue(product.update_stock(25))
            self.assertEqual(product.get_stock(), 25)
            self.assertFalse(product.update_stock(-1))  # same rejection as Product
            self.assertEqual(product.get_stock(), 25)

    def test_polymorphic_calls_through_product_collection(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.os)
        results = [product.get_fulfilment_info() for product in inventory.get_products()]
        self.assertIn("physical shipping", results[0])
        self.assertIn("delivered digitally", results[1])
        output = io.StringIO()
        with redirect_stdout(output):
            inventory.display_all()
        self.assertIn("Type: Physical", output.getvalue())
        self.assertIn("Type: Digital", output.getvalue())

    def test_json_save_and_load_keep_suppliers_shared(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.os)
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with redirect_stdout(io.StringIO()):
                save_inventory(inventory, {}, path)
                loaded, suppliers = load_inventory(path)
        guitar, os_product = loaded.find_product("P100"), loaded.find_product("D100")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertIsInstance(os_product, DigitalProduct)
        self.assertIs(guitar.get_supplier(), os_product.get_supplier())
        self.assertIs(suppliers["S001"], guitar.get_supplier())


if __name__ == "__main__":
    unittest.main(verbosity=2)
