import uuid

from typing import List

from src.exceptions.BadRequestException import BadRequestException
from src.exceptions.NotFoundException import NotFoundException
from src.exceptions.SeatPermanentlyUnavilableException import SeatPermanentlyUnavailableException
from src.models.Booking import Booking
from src.models.BookingStatus import BookingStatus
from src.models.Seat import Seat
from src.models.Show import Show
from src.providers.iSeatLockProvider import iSeatLockProvider


class BookingService:

    def __init__(self, seat_lock_provider: iSeatLockProvider):
        self.seat_lock_provider: iSeatLockProvider = seat_lock_provider
        self.show_bookings: dict[str: Booking] = {}

    def get_booking(self, booking_id: str) -> Booking:
        if booking_id not in self.show_bookings:
            raise NotFoundException()
        return self.show_bookings.get(booking_id)

    def get_all_bookings(self, show: Show) -> List[Booking]:
        response: List[Booking] = []
        for booking in self.show_bookings.values():
            if booking.show == show:
                response.append(booking)
        return response

    def create_booking(self, user_id: str, show: Show, seats: List[Seat]) -> Booking:
        if self.is_any_seat_already_booked(show, seats):
            raise SeatPermanentlyUnavailableException()
        self.seat_lock_provider.lock_seats(show, seats, user_id)
        booking_id: str = uuid.uuid4().hex
        new_booking: Booking = Booking(booking_id, show, user_id, seats)
        self.show_bookings[booking_id] = new_booking
        return new_booking

    def get_booked_seats(self, show: Show) -> List[Seat]:
        booked_seats: List[Seat] = []
        for booking in self.get_all_bookings(show):
            if booking.booking_status == BookingStatus.Confirmed:
                booked_seats.extend(booking.seats_booked)
        return booked_seats

    def confirm_booking(self, booking: Booking, user: str):
        if booking.user != user:
            raise BadRequestException()

        for seat in booking.seats_booked:
            if not self.seat_lock_provider.validate_lock(booking.show, seat, user):
                raise BadRequestException()
        booking.confirm_booking()

    def is_any_seat_already_booked(self, show: Show, seats: List[Seat]) -> bool:
        booked_seats: List[Seat] = self.get_booked_seats(show)
        for seat in seats:
            if seat in booked_seats:
                return True
        return False
