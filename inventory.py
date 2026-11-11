from product import Product


class Inventory:
    """Manages a collection of Product objects and the history of changes to it.

    Aggregation: the Inventory groups Products but does not create or own them.
    Removing a Product only removes the reference; the Product itself still exists.
    """

    def __init__(self) -> None:
        # Typed with the base class so any Product subclass can be stored
        self.__products: list[Product] = []
        self.__history: list[dict[str, str | int]] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        self.__record_transaction(product.get_product_id(), "add", product.get_stock())
        return True

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is None:
            return None
        self.__products.remove(product)
        self.__record_transaction(product.get_product_id(), "remove", product.get_stock())
        # Hand the Product back so it can be used elsewhere, e.g. added to another Inventory
        return product

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None

    def update_stock(self, product_id: str, new_stock: int) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        change = new_stock - product.get_stock()
        if not product.update_stock(new_stock):
            return False
        self.__record_transaction(product.get_product_id(), "update", change)
        return True

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        # Polymorphism: each Product runs its own display_information()
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def get_products(self) -> list[Product]:
        # Return a copy so callers cannot change the internal list directly
        return list(self.__products)

    def get_history(self) -> list[dict[str, str | int]]:
        return list(self.__history)

    def load_history(self, history: list[dict[str, str | int]]) -> None:
        self.__history = list(history)

    def __record_transaction(self, product_id: str, action: str, amount: int) -> None:
        self.__history.append({"id": product_id, "action": action, "amount": amount})
