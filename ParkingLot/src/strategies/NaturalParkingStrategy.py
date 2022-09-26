from sortedcontainers import SortedSet

from src.exceptions.NoFreeSlotAvailableException import NoFreeSlotAvailableException
from src.strategies.iParkingStrategy import iParkingStrategy


class NaturalParkingStrategy(iParkingStrategy):

    def __init__(self):
        # Python sortedcontainers
        self.slots: SortedSet = SortedSet()

    def add_slots(self, slot_number: int):
        self.slots.add(slot_number)

    def remove_slots(self, slot_number: int):
        self.slots.remove(slot_number)

    def get_next_slot(self) -> int:
        if len(self.slots) == 0:
            raise NoFreeSlotAvailableException()
        return self.slots.__getitem__(0)

# slots = NaturalParkingStrategy()
# slots.add_slots(3)
# slots.add_slots(30)
# slots.add_slots(5)
#
#
# print(slots.get_next_slot())
# slots.remove_slots(3)
# print(slots.get_next_slot())