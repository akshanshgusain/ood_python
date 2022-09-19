from typing import List

from src.models.Seat import Seat
from src.models.Show import Show
from src.services.BookingService import BookingService
from src.services.ShowService import ShowService
from src.services.TheaterService import TheaterService


class BookingController:
    def __init__(self, show_service: ShowService,
                booking_service: BookingService,
                theater_service: TheaterService):
        self.show_service: ShowService = show_service
        self.booking_service: BookingService = booking_service
        self.theater_service: TheaterService = theater_service

    def create_booking(self, user_id: str, show_id: str, seats_ids: List[str]) -> str:
        show: Show = self.show_service.get_show(show_id)
        seats: List[Seat] = []
        for seat_id in seats_ids:
            seats.append(self.theater_service.get_seat(seat_id))
        return self.booking_service.create_booking(user_id, show, seats).id
