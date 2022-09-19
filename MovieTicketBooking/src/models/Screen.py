from typing import List

from src.models.Seat import Seat


class Screen:
    def __init__(self, id: str, name: str, theater_id: str):
        self.id = id
        self.name = name
        self.theater_id: str = theater_id
        self.seats: List[Seat] = []

    def add_seat(self, seat: Seat):
        self.seats.append(seat)
