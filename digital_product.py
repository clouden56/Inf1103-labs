from product import Product


class DigitalProduct(Product):
    """A product that is delivered by download, so it has a download size."""

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        print(f"ID: {self.get_product_id()} | Name: {self.get_name()} | "
              f"Price: ${self.get_price():.2f} | Stock: {self.get_stock()}")
        print(f"    Type: Digital | Download Size: {self.__download_size:.2f} MB")
