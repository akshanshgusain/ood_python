from src.exceptions.BadRequestException import BadRequestException
from src.models.Booking import Booking
from src.providers.iSeatLockProvider import iSeatLockProvider


class PaymentsService:
    def __init__(self, allowed_retries: int, seat_lock_provider: iSeatLockProvider):
        self.allowed_retries: int = allowed_retries
        self.seat_lock_provider: iSeatLockProvider = seat_lock_provider
        self.booking_failures = {}

    def process_payment_failure(self, booking: Booking, user: str):
        if booking.user != user:
            raise BadRequestException()
        if booking not in self.booking_failures:
            self.booking_failures[booking] = 0

        current_failure_count: int = self.booking_failures.get(booking)
        new_failure_count: int = current_failure_count + 1
        self.booking_failures[booking] = new_failure_count

        if new_failure_count > self.allowed_retries:
            self.seat_lock_provider.unlock_seats(booking.show, booking.seats_booked, booking.user)
