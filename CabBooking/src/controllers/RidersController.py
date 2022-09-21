from src.models.Location import Location
from src.models.Rider import Rider
from src.models.Trip import Trip
from src.services import RidersService
from src.services.TripsService import TripsService


class RidersController:

    def __init__(self, riders_service: RidersService, trips_service: TripsService):
        self.riders_service: RidersService = riders_service
        self.trips_service: TripsService = trips_service

    def register_rider(self, rider_id: str, rider_name: str):
        self.riders_service.create_rider(Rider(rider_id, rider_name))

    def book_rider(self, rider_id: str, source_x: float, source_y: float, dest_x: float, dest_y: float) -> Trip:
        return self.trips_service.create_trip(self.riders_service.get_rider(rider_id), Location(source_x, source_y),
                                              Location(dest_x, dest_y))

    def get_history(self, rider_id: str) -> list[Trip]:
        return self.trips_service.trip_history(self.riders_service.get_rider(rider_id))


