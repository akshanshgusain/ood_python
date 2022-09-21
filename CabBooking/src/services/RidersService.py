from src.exceptions.RiderAlreadyExistsException import RiderAlreadyExistsException
from src.exceptions.RiderNotFoundException import RiderNotFoundException
from src.models.Rider import Rider


class RidersService:
    def __init__(self):
        self.riders: dict[str: Rider] = {}

    def create_rider(self, rider: Rider):
        if rider.id in self.riders:
            raise RiderAlreadyExistsException()
        self.riders[rider.id] = rider

    def get_rider(self, rider_id: str) -> Rider:
        if rider_id not in self.riders:
            raise RiderNotFoundException()
        return self.riders.get(rider_id)
