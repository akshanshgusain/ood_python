import uuid

from src.models.Cab import Cab
from src.models.Location import Location
from src.models.Rider import Rider
from src.models.TripStatus import TripStatus


class Trip:

    def __init__(self, rider: Rider, cab: Cab, price: float, from_point: Location, to_point: Location):
        self.id = uuid.uuid4().hex
        self.rider: Rider = rider
        self.cab: Cab = cab
        self.price: float = price
        self.from_point: Location = from_point
        self.to_point: Location = to_point
        self.status: TripStatus = TripStatus.IN_PROGRESS

    def end_trip(self):
        self.status = TripStatus.FINISHED
