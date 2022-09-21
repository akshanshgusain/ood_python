from abc import ABC, abstractmethod

from src.models.Cab import Cab
from src.models.Location import Location
from src.models.Rider import Rider


class iCabMatchingStrategy(ABC):

    @abstractmethod
    def match_cab_to_ride(self,
                          rider: Rider,
                          candidates_cabs: list[Cab],
                          from_point: Location,
                          to_from: Location):
        pass
