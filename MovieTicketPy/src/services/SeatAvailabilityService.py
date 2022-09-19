from typing import List

from src.models.Seat import Seat
from src.models.Show import Show
from src.providers.iSeatLockProvider import iSeatLockProvider
from src.services.BookingService import BookingService


class SeatAvailabilityService:

    def __init__(self, booking_service: BookingService,
                 seat_lock_provider: iSeatLockProvider):
        self.booking_service: BookingService = booking_service
        self.seat_lock_provider: iSeatLockProvider = seat_lock_provider

    def get_available_seats(self, show: Show) -> List[Seat]:
        all_seats: List[Seat] = show.screen.seats
        unavailable_seats: List[Seat] = self.get_unavailable_seats(show)

        available_seats: List[Seat] = []
        for seat in all_seats:
            if seat not in unavailable_seats:
                available_seats.append(seat)
        return available_seats

    def get_unavailable_seats(self, show: Show) -> List[Seat]:
        unavailable_seats: List[Seat] = self.booking_service.get_booked_seats(show)
        unavailable_seats.extend(self.seat_lock_provider.get_lock_seats(show))
        return unavailable_seats
