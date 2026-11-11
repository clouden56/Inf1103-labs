import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from can_be_shipped import CanBeShipped
from digital_product import DigitalProduct
from inventory import Inventory
from inventory_storage import load_inventory, save_inventory
from physical_product import PhysicalProduct
from product import Product
from supplier import Supplier


def captured_display(product):
    output = io.StringIO()
    with redirect_stdout(output):
        product.display_information()
    return output.getvalue()


class TestLab07(unittest.TestCase):

    def setUp(self):
        self.supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example.com")
        self.guitar = PhysicalProduct("P100", "Guitar", 350.00, 5, self.supplier, 4.2)
        self.os = DigitalProduct("D100", "Operating System", 139.00, 50, self.supplier, 5200)

    def test_physical_product_stores_and_displays_weight(self):
        self.assertEqual(self.guitar.get_weight(), 4.2)
        output = captured_display(self.guitar)
        self.assertIn("ID: P100 | Name: Guitar | Price: $350.00 | Stock: 5", output)  # from Product
        self.assertIn("Weight: 4.20 kg", output)  # from PhysicalProduct

    def test_digital_product_stores_and_displays_download_size(self):
        self.assertEqual(self.os.get_download_size(), 5200)
        output = captured_display(self.os)
        self.assertIn("ID: D100 | Name: Operating System", output)  # from Product
        self.assertIn("Download Size: 5200.00 MB", output)  # from DigitalProduct

    def test_both_subclasses_implement_get_fulfilment_info(self):
        self.assertIn("physical shipping", self.guitar.get_fulfilment_info())
        self.assertIn("digitally", self.os.get_fulfilment_info())

    def test_abstract_product_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Product("P000", "Generic", 1.00, 1, self.supplier)

    def test_physical_products_calculate_shipping_cost(self):
        self.assertIsInstance(self.guitar, CanBeShipped)
        self.assertEqual(PhysicalProduct("P1", "Mouse", 25.5, 1, self.supplier, 0.1).calculate_shipping_cost(), 5.20)
        self.assertEqual(PhysicalProduct("P2", "Laptop", 1200, 1, self.supplier, 2.0).calculate_shipping_cost(), 9.00)
        self.assertEqual(PhysicalProduct("P3", "Chair", 150, 1, self.supplier, 18.0).calculate_shipping_cost(), 41.00)

    def test_digital_products_do_not_implement_shipping(self):
        self.assertNotIsInstance(self.os, CanBeShipped)
        self.assertFalse(hasattr(self.os, "calculate_shipping_cost"))

    def test_inventory_operations_work_with_both_types(self):
        inventory = Inventory()
        self.assertTrue(inventory.add_product(self.guitar))
        self.assertTrue(inventory.add_product(self.os))
        self.assertFalse(inventory.add_product(DigitalProduct("p100", "Duplicate", 1, 1, self.supplier, 1)))
        self.assertIs(inventory.find_product("d100"), self.os)
        self.assertTrue(inventory.update_stock("P100", 9))
        self.assertEqual(self.guitar.get_stock(), 9)
        self.assertFalse(inventory.update_stock("P100", -1))

    def test_json_save_and_load_preserve_product_types(self):
        inventory = Inventory()
        inventory.add_product(self.guitar)
        inventory.add_product(self.os)
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "inventory.json")
            with redirect_stdout(io.StringIO()):
                save_inventory(inventory, {}, path)
                loaded, _ = load_inventory(path)

        guitar = loaded.find_product("P100")
        os_product = loaded.find_product("D100")
        self.assertIsInstance(guitar, PhysicalProduct)
        self.assertEqual(guitar.get_weight(), 4.2)
        self.assertIsInstance(os_product, DigitalProduct)
        self.assertEqual(os_product.get_download_size(), 5200)
        self.assertEqual(loaded.get_history(), inventory.get_history())


if __name__ == "__main__":
    unittest.main(verbosity=2)
