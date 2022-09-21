from src.models.Cab import Cab
from src.models.Location import Location
from src.services.CabsService import CabsService
from src.services.TripsService import TripsService


class CabsController:

    def __init__(self, cabs_service: CabsService, trips_service: TripsService):
        self.cabs_service: CabsService = cabs_service
        self.trips_service: TripsService = trips_service

    def register_cab(self, cab_id: str, driver_name: str):
        self.cabs_service.create_cab(Cab(cab_id, driver_name))

    def update_cab_location(self, cab_id: str, new_x: float, new_y: float):
        self.cabs_service.update_cab_location(cab_id, Location(new_x, new_y))

    def update_cab_availability(self, cab_id: str, new_availability: bool):
        self.cabs_service.update_cab_availability(cab_id, new_availability)

    def end_trip(self, cab_id: str):
        self.trips_service.end_trip(self.cabs_service.get_cab(cab_id))
