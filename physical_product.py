from can_be_shipped import CanBeShipped
from product import Product
from supplier import Supplier


class PhysicalProduct(Product, CanBeShipped):
    """A product that is stored and shipped, so it has a weight.

    Inherits from one class (Product) and implements one interface (CanBeShipped).
    """

    BASE_SHIPPING_COST: float = 5.00
    SHIPPING_COST_PER_KG: float = 2.00

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        # Overrides Product: the parent prints the common details, this adds the weight
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg")

    def get_fulfilment_info(self) -> str:
        return (f"This product requires physical shipping "
                f"(shipping cost: ${self.calculate_shipping_cost():.2f}).")

    def calculate_shipping_cost(self) -> float:
        # Simple rule: a flat base fee plus a charge for every kilogram
        cost = self.BASE_SHIPPING_COST + self.SHIPPING_COST_PER_KG * self.__weight
        return round(cost, 2)
