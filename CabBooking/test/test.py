import unittest
import uuid

from src.controllers.CabsControlle import CabsController
from src.controllers.RidersController import RidersController
from src.exceptions.CabAlreadyExistsException import CabAlreadyExistsException
from src.exceptions.CabNotFoundException import CabNotFoundException
from src.exceptions.NoCabsAvailableException import NoCabsAvailableException
from src.exceptions.RiderAlreadyExistsException import RiderAlreadyExistsException
from src.exceptions.RiderNotFoundException import RiderNotFoundException
from src.services.CabsService import CabsService
from src.services.RidersService import RidersService
from src.services.TripsService import TripsService
from src.strategies.DefaultCabMatchingStrategy import DefaultCabMatchingStrategy
from src.strategies.DefaultPricingStrategy import DefaultPricingStrategy
from src.strategies.iCabMatchingStrategy import iCabMatchingStrategy
from src.strategies.iPricingStrategy import iPricingStrategy


class BaseTest(unittest.TestCase):
    cab_controller: CabsController
    riders_controller: RidersController

    def setUp(self) -> None:
        # Strategies
        self.cab_matching_strategy: iCabMatchingStrategy = DefaultCabMatchingStrategy()
        self.pricing_strategy: iPricingStrategy = DefaultPricingStrategy()

        # Service Objects
        self.cabs_service: CabsService = CabsService()
        self.riders_service: RidersService = RidersService()
        self.trips_service: TripsService = TripsService(self.cabs_service, self.riders_service,
                                                        self.cab_matching_strategy, self.pricing_strategy)

        # Controllers
        self.cab_controller = CabsController(self.cabs_service, self.trips_service)
        self.riders_controller = RidersController(self.riders_service, self.trips_service)

    @classmethod
    def gen_id(cls) -> str:
        return uuid.uuid4().hex

    def test_case_01(self):
        rider_id_1: str = self.gen_id()
        self.riders_controller.register_rider(rider_id_1, "Umesh")
        rider_id_2: str = self.gen_id()
        self.riders_controller.register_rider(rider_id_2, "Chetan")
        rider_id_3: str = self.gen_id()
        self.riders_controller.register_rider(rider_id_3, "Gaurav")
        rider_id_4: str = self.gen_id()
        self.riders_controller.register_rider(rider_id_4, "Zayan")

        cab_id_1: str = self.gen_id()
        self.cab_controller.register_cab(cab_id_1, "Singh")
        cab_id_2: str = self.gen_id()
        self.cab_controller.register_cab(cab_id_2, "Negi")
        cab_id_3: str = self.gen_id()
        self.cab_controller.register_cab(cab_id_3, "Sharma")
        cab_id_4: str = self.gen_id()
        self.cab_controller.register_cab(cab_id_4, "Patel")
        cab_id_5: str = self.gen_id()
        self.cab_controller.register_cab(cab_id_5, "Yadav")

        # Give Locations to cabs
        self.cab_controller.update_cab_location(cab_id_1, 1, 1)
        self.cab_controller.update_cab_location(cab_id_2, 2, 2)
        self.cab_controller.update_cab_location(cab_id_3, 100, 100)
        self.cab_controller.update_cab_location(cab_id_4, 110, 110)
        self.cab_controller.update_cab_location(cab_id_5, 4, 4)

        # Give Availability to cabs
        self.cabs_service.update_cab_availability(cab_id_2, False)
        self.cabs_service.update_cab_availability(cab_id_4, False)

        # Book Cabs for Rider
        self.riders_controller.book_rider(rider_id_1, 0, 0, 500, 500)
        self.riders_controller.book_rider(rider_id_2, 0, 0, 500, 500)

        print(f"\n### Printing current trips for rider_id_1 :{rider_id_1} and rider_id_2: {rider_id_2}")
        print(self.riders_controller.get_history(rider_id_1))
        print(self.riders_controller.get_history(rider_id_2))

        self.cab_controller.update_cab_location(cab_id_5, 50, 50)

        print(f"\n### Printing current trips for rider_id_1 :{rider_id_1} and rider_id_2: {rider_id_2}")
        print(self.riders_controller.get_history(rider_id_1))
        print(self.riders_controller.get_history(rider_id_2))

        self.cab_controller.end_trip(cab_id_5)

        print(f"\n### Printing current trips for rider_id_1 :{rider_id_1} and rider_id_2: {rider_id_2}")
        print(self.riders_controller.get_history(rider_id_1))
        print(self.riders_controller.get_history(rider_id_2))

        with self.assertRaises(NoCabsAvailableException):
            self.riders_controller.book_rider(rider_id_3, 0, 0, 500, 500)

        self.riders_controller.book_rider(rider_id_4, 48, 48, 500, 500)
        print(
            f"\n### Printing current trips for rider_id_1 :{rider_id_1} and rider_id_2: {rider_id_2} and rider_id_4: {rider_id_4}")
        print(self.riders_controller.get_history(rider_id_1))
        print(self.riders_controller.get_history(rider_id_2))
        print(self.riders_controller.get_history(rider_id_4))

        with self.assertRaises(RiderNotFoundException):
            self.riders_controller.book_rider(self.gen_id(), 0, 0, 500, 500)

        with self.assertRaises(RiderAlreadyExistsException):
            self.riders_controller.register_rider(rider_id_1, "Bhist")

        with self.assertRaises(CabAlreadyExistsException):
            self.cab_controller.register_cab(cab_id_3, "Ashwani")

        with self.assertRaises(CabNotFoundException):
            self.cab_controller.update_cab_location(self.gen_id(), 110, 89)

        with self.assertRaises(CabNotFoundException):
            self.cab_controller.update_cab_availability(self.gen_id(), False)


