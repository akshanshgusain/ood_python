from datetime import datetime
from typing import List

from src.controllers.BookingConstroller import BookingController
from src.controllers.MovieController import MovieController
from src.controllers.PaymentsController import PaymentsController
from src.controllers.ShowController import ShowController
from src.controllers.TheaterController import TheaterController
from src.models.Screen import Screen
from src.providers.InMemorySeatLockProvider import InMemorySeatLockProvider
from src.providers.iSeatLockProvider import iSeatLockProvider
from src.services.BookingService import BookingService
from src.services.MovieService import MovieService
from src.services.PaymentsSerivce import PaymentsService
from src.services.SeatAvailabilityService import SeatAvailabilityService
from src.services.ShowService import ShowService
from src.services.TheaterService import TheaterService


def create_seats(theater_controller_: TheaterController, screen_: str, num_row: int, num_seats_in_rows: int) -> List[
    str]:
    seats: List[str] = []
    for row in range(num_row):
        for seat_no in range(num_seats_in_rows):
            seat = theater_controller_.create_seats_in_screen(row, seat_no, screen_)
            seats.append(seat)
    return seats


def setup_screen(theater_controller_: TheaterController, ) -> str:
    theater: str = theater_controller_.create_theater("Theater 1")
    return theater_controller_.create_screen_in_theater("Screen 1", theater)


def validate_seats_list(seats_list: List[str], all_seats_in_screen: List[str],
                        excluded_seats: List[str]) -> bool:
    inc_seats: bool = False

    exc_seats: bool = False

    for included_seat in all_seats_in_screen:
        if included_seat not in excluded_seats:
            inc_seats = included_seat in seats_list

    for excluded_seat in excluded_seats:
        exc_seats = excluded_seat in seats_list

    print(f"{inc_seats} - {exc_seats}")
    return inc_seats and exc_seats


if __name__ == "__main__":
    lock_timeout: int = 10
    allowed_retries: int = 0

    # Create Services to be injected into controllers
    seat_lock_provider: iSeatLockProvider = InMemorySeatLockProvider(lock_timeout)
    booking_service: BookingService = BookingService(seat_lock_provider)
    movie_service: MovieService = MovieService()
    show_service: ShowService = ShowService()
    theater_service: TheaterService = TheaterService()
    seat_availability_service: SeatAvailabilityService = \
        SeatAvailabilityService(booking_service, seat_lock_provider)
    payment_service: PaymentsService = PaymentsService(allowed_retries, seat_lock_provider)

    # Initialise Controllers
    booking_controller = BookingController(show_service, booking_service, theater_service)
    show_controller = ShowController(seat_availability_service, show_service, theater_service,
                                     movie_service)
    theater_controller = TheaterController(theater_service)
    movie_controller = MovieController(movie_service)
    payments_controller = PaymentsController(payment_service, booking_service)

    print("test case 1")
    user_1: str = "User1"
    user_2: str = "User2"

    movie: str = movie_controller.create_movie("Movie 1")
    screen: str = setup_screen(theater_controller)
    screen1_seat_ids: List[str] = create_seats(theater_controller, screen, 2, 10)
    print(screen1_seat_ids)

    show_id: str = show_controller.create_show(movie, screen, datetime.now(), 2 * 60 * 60)
    print(f"Main: show id: {show_id}")

    show_d = show_service.shows
    # print("ALL SHOWS: ")
    # for show in show_d.values():
    #     print(f"SHOW:  {show}")
    #     for seat in show.screen.seats:
    #         print(f"  SEAT: {seat}")
    screens: dict[str: Screen] = theater_service.screens
    print("ALL SCREENS")
    for key, value in screens.items():
        print(value)
        print(type(value))
        for seat in value.seats:
            print(seat)

    user_1_available_seats: List[str] = show_controller.get_available_seats(show_id)
    print(user_1_available_seats)

    if validate_seats_list(user_1_available_seats, screen1_seat_ids, []):
        print(f'1 .Seats validated')
    else:
        print(f'1 .Seats NOT validated')
