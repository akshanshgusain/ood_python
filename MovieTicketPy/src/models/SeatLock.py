from dataclasses import dataclass
from datetime import datetime, timedelta, time
from time import sleep

from src.models.Seat import Seat
from src.models.Show import Show


@dataclass
class SeatLock:
    seat: Seat
    show: Show
    timeout_in_seconds: int
    lock_time: datetime

    locked_by: str

    def is_lock_expired(self) -> bool:
        lock_instant: time = (self.lock_time + timedelta(seconds=self.timeout_in_seconds)).time()
        current_instant: time = datetime.now().time()
        return lock_instant <= current_instant

# def check_lock(seat_lock):
#     if seat_lock.is_lock_expired():
#         print("True")
#     else:
#         print("False")


# if __name__ == "__main__":
#     seat_lock = SeatLock(6, datetime.now())
#     check_lock(seat_lock)
#     sleep(3)
#     check_lock(seat_lock)
#     sleep(3)
#     check_lock(seat_lock)
