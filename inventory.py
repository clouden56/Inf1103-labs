class Inventory:
    """Manages a collection of Product objects and the history of changes to it."""

    def __init__(self):
        self.__products = []
        self.__history = []

    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        self.__record_transaction(product.get_product_id(), "add", product.get_stock())
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None

    def update_stock(self, product_id, new_stock):
        product = self.search_product(product_id)
        if product is None:
            return False
        change = new_stock - product.get_stock()
        if not product.update_stock(new_stock):
            return False
        self.__record_transaction(product.get_product_id(), "update", change)
        return True

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print("-" * 48)

    def get_products(self):
        # Return a copy so callers cannot change the internal list directly
        return list(self.__products)

    def get_history(self):
        return list(self.__history)

    def load_history(self, history):
        self.__history = list(history)

    def __record_transaction(self, product_id, action, amount):
        self.__history.append({"id": product_id, "action": action, "amount": amount})
