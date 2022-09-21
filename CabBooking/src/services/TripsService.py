from src.exceptions.NoCabsAvailableException import NoCabsAvailableException
from src.exceptions.TripNotFoundException import TripNotFoundException
from src.models.Cab import Cab
from src.models.Location import Location
from src.models.Rider import Rider
from src.models.Trip import Trip
from src.services.CabsService import CabsService
from src.services.RidersService import RidersService
from src.strategies.iCabMatchingStrategy import iCabMatchingStrategy
from src.strategies.iPricingStrategy import iPricingStrategy


class TripsService:
    MAX_ALLOWED_TRIP_MATCHING_DISTANCE: float = 10

    def __init__(self, cabs_service: CabsService, riders_service: RidersService,
                 cab_matching_strategy: iCabMatchingStrategy, pricing_strategy: iPricingStrategy):
        self.trips: dict[str: list[Trip]] = {}  # [rider_id: list[Trip]]

        self.trips_by_id: dict[str: Trip] = {}

        self.cabs_service: CabsService = cabs_service
        self.riders_service: RidersService = riders_service
        self.cab_matching_strategy: iCabMatchingStrategy = cab_matching_strategy
        self.pricing_strategy: iPricingStrategy = pricing_strategy

    def create_trip(self, rider: Rider, from_point: Location, to_point: Location):
        close_by_cabs: list[Cab] = self.cabs_service.get_cabs(from_point, self.MAX_ALLOWED_TRIP_MATCHING_DISTANCE)
        close_by_available_cabs: list[Cab] = []
        for cab in close_by_cabs:
            if cab.current_trip_id == "-90":
                close_by_available_cabs.append(cab)
        selected_cab: Cab = self.cab_matching_strategy.match_cab_to_ride(rider, close_by_available_cabs, from_point,
                                                                         to_point)
        if selected_cab is None:
            raise NoCabsAvailableException()

        price: float = self.pricing_strategy.find_price(from_point, to_point)
        new_trip: Trip = Trip(rider, selected_cab, price, from_point, to_point)
        if rider.id not in self.trips:
            self.trips[rider.id] = []
        self.trips.get(rider.id).append(new_trip)

        self.trips_by_id[new_trip.id] = new_trip

        selected_cab.current_trip_id = new_trip.id

    def trip_history(self, rider: Rider) -> list[Trip]:
        # for trip in self.trips.values():
        #     for tp in trip:
        #         print(f"Trip ID: {tp.id}")
        #         print(f"Rider ID: {tp.rider.id}")
        return self.trips.get(rider.id)

    def end_trip(self, cab: Cab):
        if cab.current_trip_id == "-90":
            raise TripNotFoundException()
        tripp: Trip = self.trips_by_id.get(cab.current_trip_id)
        tripp.end_trip()
        cab.current_trip_id = "-90"
