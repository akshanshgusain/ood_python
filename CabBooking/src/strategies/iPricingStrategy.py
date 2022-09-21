from abc import ABC, abstractmethod

from src.models.Location import Location


class iPricingStrategy(ABC):

    @abstractmethod
    def find_price(self, from_point: Location, to_point: Location):
        pass
