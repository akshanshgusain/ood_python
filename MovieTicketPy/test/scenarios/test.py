import unittest
from datetime import datetime
from typing import List

from src.controllers.BookingConstroller import BookingController
from src.controllers.MovieController import MovieController
from src.controllers.PaymentsController import PaymentsController
from src.controllers.ShowController import ShowController
from src.controllers.TheaterController import TheaterController
from src.exceptions.SeatPermanentlyUnavilableException import SeatPermanentlyUnavailableException
from src.exceptions.SeatTemporaryUnavailableException import SeatTemporaryUnavailableException
from src.providers.InMemorySeatLockProvider import InMemorySeatLockProvider
from src.providers.iSeatLockProvider import iSeatLockProvider
from src.services.BookingService import BookingService
from src.services.MovieService import MovieService
from src.services.PaymentsSerivce import PaymentsService
from src.services.SeatAvailabilityService import SeatAvailabilityService
from src.services.ShowService import ShowService
from src.services.TheaterService import TheaterService


class BaseTest(unittest.TestCase):
    seat_lock_provider: iSeatLockProvider
    booking_service: BookingService
    movie_service: MovieService
    show_service: ShowService
    theater_service: TheaterService
    seat_availability_service: SeatAvailabilityService
    payment_service: PaymentsService

    booking_controller: BookingController
    show_controller: ShowController
    theater_controller: TheaterController
    movie_controller: MovieController
    payments_controller: PaymentsController

    @classmethod
    def setup_controllers(cls, lock_timeout: int, allowed_retries: int):
        # Create Services to be injected into controllers
        cls.seat_lock_provider: iSeatLockProvider = InMemorySeatLockProvider(lock_timeout)
        cls.booking_service: BookingService = BookingService(cls.seat_lock_provider)
        cls.movie_service: MovieService = MovieService()
        cls.show_service: ShowService = ShowService()
        cls.theater_service: TheaterService = TheaterService()
        cls.seat_availability_service: SeatAvailabilityService = \
            SeatAvailabilityService(cls.booking_service, cls.seat_lock_provider)
        cls.payment_service: PaymentsService = PaymentsService(allowed_retries, cls.seat_lock_provider)

        # Initialise Controllers
        # Controllers
        cls.booking_controller = BookingController(cls.show_service, cls.booking_service, cls.theater_service)
        cls.show_controller = ShowController(cls.seat_availability_service, cls.show_service, cls.theater_service,
                                             cls.movie_service)
        cls.theater_controller = TheaterController(cls.theater_service)
        cls.movie_controller = MovieController(cls.movie_service)
        cls.payments_controller = PaymentsController(cls.payment_service, cls.booking_service)

    @classmethod
    def create_seats(cls, screen: str, num_row: int, num_seats_in_rows: int) -> List[str]:
        seats: List[str] = []
        for row in range(num_row):
            for seat_no in range(num_seats_in_rows):
                seat = cls.theater_controller.create_seats_in_screen(row, seat_no, screen)
                seats.append(seat)
        return seats

    @classmethod
    def setup_screen(cls) -> str:
        theater: str = cls.theater_controller.create_theater("Theater 1")
        return cls.theater_controller.create_screen_in_theater("Screen 1", theater)

    @classmethod
    def validate_included_seats_list(cls, seats_list: List[str], all_seats_in_screen: List[str],
                                     excluded_seats: List[str]) -> bool:

        for included_seat in all_seats_in_screen:
            if included_seat not in excluded_seats:
                return included_seat in seats_list

    @classmethod
    def validate_excluded_seats_list(cls, seats_list: List[str], all_seats_in_screen: List[str],
                                     excluded_seats: List[str]) -> bool:

        for excluded_seat in excluded_seats:
            return excluded_seat in seats_list

    def setUp(self):
        self.setup_controllers(10, 0)

    def test_case_01(self):

        print("test case 1")

        user_1: str = "User1"

        movie: str = self.movie_controller.create_movie("Movie 1")
        screen: str = self.setup_screen()
        screen1_seat_ids: List[str] = self.create_seats(screen, 2, 10)

        show: str = self.show_controller.create_show(movie, screen, datetime.now(), 2 * 60 * 60)

        user_1_available_seats: List[str] = self.show_controller.get_available_seats(show)

        # Validate that seats u1 received has all screen seats
        self.assertTrue(self.validate_included_seats_list(user_1_available_seats, screen1_seat_ids, []))
        self.assertFalse(self.validate_excluded_seats_list(user_1_available_seats, screen1_seat_ids, []))

        # Create Booking for user 1
        user_1_selected_seats = [screen1_seat_ids[0], screen1_seat_ids[1], screen1_seat_ids[2], screen1_seat_ids[3]]
        booking_id: str = self.booking_controller.create_booking(user_1, show, user_1_selected_seats)
        self.payments_controller.payment_success(booking_id, user_1)

        # Get available seats for user 2
        user_2_available_seats: List[str] = self.show_controller.get_available_seats(show)
        self.assertTrue(
            self.validate_included_seats_list(user_2_available_seats, screen1_seat_ids, user_1_selected_seats))

    def test_case_02(self):

        print("test case 2")
        user_1: str = "User1"
        user_2: str = "User2"

        movie: str = self.movie_controller.create_movie("Movie 2")
        screen: str = self.setup_screen()
        screen1_seat_ids: List[str] = self.create_seats(screen, 2, 10)
        show: str = self.show_controller.create_show(movie, screen, datetime.now(), 2 * 60 * 60)

        user_1_available_seats: List[str] = self.show_controller.get_available_seats(show)

        # Validate that seats u1 received has all screen seats
        self.assertTrue(self.validate_included_seats_list(user_1_available_seats, screen1_seat_ids, []))
        self.assertFalse(self.validate_excluded_seats_list(user_1_available_seats, screen1_seat_ids, []))

        # Create Booking for user 1 But. Don't complete the payment
        user_1_selected_seats = [screen1_seat_ids[0], screen1_seat_ids[1], screen1_seat_ids[2], screen1_seat_ids[3]]
        booking_id: str = self.booking_controller.create_booking(user_1, show, user_1_selected_seats)

        # Get Seats available for User 2
        user_2_available_seats: List[str] = self.show_controller.get_available_seats(show)
        # validate that user 2 seats has all the seats except the ones already blocked by user 1
        self.assertTrue(
            self.validate_included_seats_list(user_2_available_seats, screen1_seat_ids, user_1_selected_seats))

        # Fail the Payment fort User 1
        self.payments_controller.payment_failed(booking_id, user_1)

        # Now again check which seats are available for user 2
        user_2_available_seats_after_payment_failure: List[str] = self.show_controller.get_available_seats(show)
        # Since User 1's payment has failed so User 2 should now get back all the seats.
        self.assertTrue(
            self.validate_included_seats_list(user_2_available_seats_after_payment_failure, screen1_seat_ids, []))

    def test_case_03(self):
        print("test case 3")
        user_1: str = "User1"
        user_2: str = "User2"

        movie: str = self.movie_controller.create_movie("Movie 2")
        screen: str = self.setup_screen()
        screen1_seat_ids: List[str] = self.create_seats(screen, 2, 10)
        show: str = self.show_controller.create_show(movie, screen, datetime.now(), 2 * 60 * 60)

        user_1_available_seats: List[str] = self.show_controller.get_available_seats(show)

        # Validate that seats u1 received has all screen seats
        self.assertTrue(self.validate_included_seats_list(user_1_available_seats, screen1_seat_ids, []))
        self.assertFalse(self.validate_excluded_seats_list(user_1_available_seats, screen1_seat_ids, []))

        # Create Seat Selection for User 1
        user_1_selected_seats = [screen1_seat_ids[0], screen1_seat_ids[2], screen1_seat_ids[5], screen1_seat_ids[9]]

        # Create Seat Selection for User 2
        user_2_selected_seats = [screen1_seat_ids[0], screen1_seat_ids[1], screen1_seat_ids[2], screen1_seat_ids[5]]

        # User 1 Proceeds to Book
        user_1_booking_id: str = self.booking_controller.create_booking(user_1, show, user_1_selected_seats)

        # User 3 Proceed to Book with Overlapping seats
        with self.assertRaises(SeatTemporaryUnavailableException):
            user_2_booking_id: str = self.booking_controller.create_booking(user_2, show, user_2_selected_seats)

        # User 1 Completes the payment, seats become permanently unavailable
        self.payments_controller.payment_success(user_1_booking_id, user_1)

        with self.assertRaises(SeatPermanentlyUnavailableException):
            user_2_booking_id: str = self.booking_controller.create_booking(user_2, show, user_2_selected_seats)
