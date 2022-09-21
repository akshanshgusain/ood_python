from src.exceptions.CabAlreadyExistsException import CabAlreadyExistsException
from src.exceptions.CabNotFoundException import CabNotFoundException
from src.models.Cab import Cab
from src.models.Location import Location


class CabsService:

    def __init__(self):
        self.cabs: dict[str: Cab] = {}

    def create_cab(self, cab: Cab):
        if cab.id in self.cabs:
            raise CabAlreadyExistsException()
        self.cabs[cab.id] = cab

    def get_cab(self, cab_id: str) -> Cab:
        if cab_id not in self.cabs:
            raise CabNotFoundException()
        return self.cabs.get(cab_id)

    def update_cab_location(self, cab_id: str, new_location: Location):
        if cab_id not in self.cabs:
            raise CabNotFoundException()
        cabb: Cab = self.cabs.get(cab_id)
        cabb.current_location = new_location

    def update_cab_availability(self, cab_id: str, new_availability: bool):
        if cab_id not in self.cabs:
            raise CabNotFoundException()
        cabb: Cab = self.cabs.get(cab_id)
        cabb.is_available = new_availability

    def get_cabs(self, from_point: Location, distance: float) -> list[Cab]:
        cabs: list[Cab] = []

        for cab in self.cabs.values():
            if cab.is_available and cab.current_location.distance(from_point) <= distance:
                cabs.append(cab)
        return cabs
