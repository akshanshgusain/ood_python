from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Seat:
    id: str
    row_number: int
    seat_number: int
