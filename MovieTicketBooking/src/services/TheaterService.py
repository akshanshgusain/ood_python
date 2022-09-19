import uuid
from src.exceptions.NotFoundException import NotFoundException
from src.models.Screen import Screen
from src.models.Seat import Seat
from src.models.Theater import Theater


class TheaterService:
    def __init__(self):
        self.theaters: dict[str: Theater] = {}
        self.screens: dict[str: Screen] = {}
        self.seats: dict[str: Seat] = {}

    # Getters
    def get_seat(self, seat_id: str) -> Seat:
        if seat_id in self.seats:
            return self.seats.get(seat_id)
        else:
            raise NotFoundException()

    def get_theater(self, theater_id: str) -> Theater:
        if theater_id in self.theaters:
            return self.theaters.get(theater_id)
        else:
            raise NotFoundException()

    def get_screen(self, screen_id: str) -> Screen:
        if screen_id in self.screens:
            return self.screens.get(screen_id)
        else:
            raise self.screens.get(screen_id)

    # Setters

    def create_theater(self, theater_name: str) -> Theater:
        theater_id: str = uuid.uuid4().hex
        theater: Theater = Theater(theater_id, theater_name)
        self.theaters[theater_id] = theater
        return theater

    def create_screen_in_theater(self, screen_name: str, theater: Theater) -> Screen:
        screen: Screen = self.create_screen(screen_name, theater)
        theater.add_screen(screen)
        return screen

    def create_seat_in_screen(self, row_no: int, seat_no: int, screen: Screen) -> Seat:
        seat_id: str = uuid.uuid4().hex
        seat: Seat = Seat(seat_id, row_no, seat_no)
        self.seats[seat_id] = seat
        screen.add_seat(seat)
        return seat

    def create_screen(self, screen_name: str, theater: Theater) -> Screen:
        screen_id: str = uuid.uuid4().hex
        screen: Screen = Screen(screen_id, screen_name, theater.id)
        self.screens[screen_id] = screen
        return screen
