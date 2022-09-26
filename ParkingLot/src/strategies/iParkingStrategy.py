from abc import ABC, abstractmethod


class iParkingStrategy(ABC):
    """"""
    """Add a new slot to parking strategy. After adding, this new slot will become available for
        future parking."""

    @abstractmethod
    def add_slots(self, slot_number: int):
        pass

    """Removes a slot from the parking strategy. After removing, this slot will not be used for future
        parking"""

    @abstractmethod
    def remove_slots(self, slot_number: int):
        pass

    """Get the next free slot as per the parking strategy."""

    @abstractmethod
    def get_next_slot(self) -> int:
        pass
