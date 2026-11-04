from product import Product


class PhysicalProduct(Product):
    """A product that is stored and shipped, so it has a weight."""

    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    def display_information(self):
        # Overrides Product: the parent prints the common details, this adds the weight
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")
