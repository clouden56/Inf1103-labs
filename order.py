from order_line import OrderLine
from product import Product


class Order:
    """A customer order that creates and manages its own OrderLine objects."""

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates the OrderLine itself; lines are never passed in from outside
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.get_product().get_product_id().upper() == product_id.upper():
                self.__order_lines.remove(order_line)
                return True
        return False

    def get_order_lines(self) -> tuple[OrderLine, ...]:
        # A tuple is read-only, so lines cannot be added or moved to another Order from outside
        return tuple(self.__order_lines)

    def calculate_total(self) -> float:
        total = 0.0
        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()
        return round(total, 2)

    def display_order(self) -> None:
        print(f"\nOrder {self.__order_id}")
        print("-" * 48)
        if not self.__order_lines:
            print("Order is empty.")
        for order_line in self.__order_lines:
            order_line.display_information()
        print("-" * 48)
        print(f"Total: ${self.calculate_total():.2f}")
