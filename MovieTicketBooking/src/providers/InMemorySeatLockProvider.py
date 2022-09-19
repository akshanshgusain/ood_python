from datetime import datetime
from typing import List

from src.exceptions.SeatTemporaryUnavailableException import SeatTemporaryUnavailableException
from src.models.Seat import Seat
from src.models.SeatLock import SeatLock
from src.models.Show import Show
from src.providers.iSeatLockProvider import iSeatLockProvider


class InMemorySeatLockProvider(iSeatLockProvider):

    def __init__(self, lock_timeout: int):
        self.locks: dict[Show: dict[Seat: SeatLock]] = {}
        self.lock_timeout = lock_timeout

    def lock_seats(self, show: Show, seats: List[Seat], user: str):
        for seat in seats:
            if self.is_seat_locked(show, seat):
                raise SeatTemporaryUnavailableException()

        for seat in seats:
            self.lock_seat(show, seat, user, self.lock_timeout)

    def unlock_seats(self, show: Show, seats: List[Seat], user: str):
        for seat in seats:
            if self.validate_lock(show, seat, user):
                self.unlock_seat(show, seat)

    def validate_lock(self, show: Show, seat: Seat, user: str) -> bool:
        return self.is_seat_locked(show, seat) and (self.locks.get(show).get(seat).locked_by == user)

    def get_lock_seats(self, show: Show) -> List[Seat]:
        if show not in self.locks:
            return []

        locked_seats: List[Seat] = []

        for seat in self.locks.get(show):
            if self.is_seat_locked(show, seat):
                locked_seats.append(seat)

        return locked_seats

    # helpers

    def unlock_seat(self, show: Show, seat: Seat):
        if show in self.locks:
            self.locks.get(show).pop(seat)
        else:
            return

    def lock_seat(self, show: Show, seat: Seat, user: str, timeout_in_seconds: int):
        if show not in self.locks:
            self.locks[show] = {}
        lock: SeatLock = SeatLock(seat, show, timeout_in_seconds, datetime.now(), user)
        self.locks.get(show)[seat] = lock

    def is_seat_locked(self, show: Show, seat: Seat) -> bool:
        return show in self.locks \
               and (seat in self.locks.get(show)) \
               and not (self.locks.get(show).get(seat).is_lock_expired())
