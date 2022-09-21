from src.models.Cab import Cab
from src.models.Location import Location
from src.models.Rider import Rider
from src.strategies.iCabMatchingStrategy import iCabMatchingStrategy


class DefaultCabMatchingStrategy(iCabMatchingStrategy):

    def match_cab_to_ride(self, rider: Rider, candidates_cabs: list[Cab], from_point: Location, to_from: Location):
        if len(candidates_cabs) == 0:
            return None

        return candidates_cabs[0]
