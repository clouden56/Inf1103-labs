from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    """Interface: any class that can be shipped must be able to work out its shipping cost."""

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass
