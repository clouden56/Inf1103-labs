from product import Product


class OrderLine:
    """One product and quantity within an Order.

    Composition: an OrderLine is only created by its Order and belongs to that one Order.
    It refers to a Product (association) but does not own it.
    """

    def __init__(self, product: Product, quantity: int) -> None:
        self.__product: Product = product
        self.__quantity: int = quantity

    def get_product(self) -> Product:
        return self.__product

    def get_quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        return round(self.__product.get_price() * self.__quantity, 2)

    def display_information(self) -> None:
        print(f"{self.__product.get_product_id()} | {self.__product.get_name()} | "
              f"{self.__quantity} x ${self.__product.get_price():.2f} = "
              f"${self.calculate_subtotal():.2f}")
