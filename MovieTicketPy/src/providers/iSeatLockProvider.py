from abc import ABC, abstractmethod
from typing import List

from src.models.Seat import Seat
from src.models.Show import Show


class iSeatLockProvider(ABC):
    @abstractmethod
    def lock_seats(self, show: Show, seat: List[Seat], user: str):
        pass

    @abstractmethod
    def unlock_seats(self, show: Show, seat: List[Seat], user: str):
        pass

    @abstractmethod
    def validate_lock(self, show: Show, seat: Seat, user: str) -> bool:
        pass

    @abstractmethod
    def get_lock_seats(self, show: Show) -> List[Seat]:
        pass
