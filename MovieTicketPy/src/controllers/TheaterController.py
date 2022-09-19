from src.models.Screen import Screen
from src.models.Theater import Theater
from src.services.TheaterService import TheaterService


class TheaterController:
    def __init__(self, theater_service: TheaterService):
        self.theater_service: TheaterService = theater_service

    # Create Theater
    def create_theater(self, theater_name: str) -> str:
        return self.theater_service.create_theater(theater_name).id

    # Create Screen in Theater
    def create_screen_in_theater(self, screen_name: str, theater_id: str) -> str:
        theater: Theater = self.theater_service.get_theater(theater_id)
        return self.theater_service.create_screen_in_theater(screen_name, theater).id

    # Create Seats in the Screen
    def create_seats_in_screen(self, row_no: int, seat_no: int, scree_id: str):
        screen: Screen = self.theater_service.get_screen(scree_id)
        return self.theater_service.create_seat_in_screen(row_no, seat_no, screen).id
