from typing import List

from src.exceptions.InvalidStateException import InvalidStateException
from src.models.BookingStatus import BookingStatus
from src.models.Seat import Seat
from src.models.Show import Show


class Booking:
    def __init__(self, id: str, show: Show, user: str, seats_booked: List[Seat]):
        self.id = id
        self.show = show
        self.user = user
        self.seats_booked: List[Seat] = seats_booked
        self.booking_status = BookingStatus.Created

    def confirm_booking(self):
        if self.booking_status != BookingStatus.Created:
            raise InvalidStateException()
        self.booking_status = BookingStatus.Confirmed

    def is_confirmed(self) -> bool:
        return self.booking_status == BookingStatus.Confirmed

    def expire_booking(self):
        if self.booking_status != BookingStatus.Created:
            raise InvalidStateException()
        self.booking_status = BookingStatus.Expired
