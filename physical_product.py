from product import Product


class PhysicalProduct(Product):
    """A product that is stored and shipped, so it has a weight."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    def display_information(self):
        print(f"ID: {self.get_product_id()} | Name: {self.get_name()} | "
              f"Price: ${self.get_price():.2f} | Stock: {self.get_stock()}")
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")
