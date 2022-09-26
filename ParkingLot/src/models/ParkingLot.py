from src.exceptions.InvalidSlotException import InvalidSlotException
from src.exceptions.ParkingLotException import ParkingLotException
from src.exceptions.SlotAlreadyOccupiedException import SlotAlreadyOccupiedException
from src.models.Car import Car
from src.models.Slot import Slot


class ParkingLot:
    MAX_CAPACITY: int = 100000

    def __init__(self, capacity: int):
        self.slots: dict[int: Slot] = {}

        if capacity > self.MAX_CAPACITY or capacity <= 0:
            raise ParkingLotException("Invalid capacity given for parking lot.")
        self.capacity: int = capacity

    def get_slot(self, slot_number: int) -> Slot:
        if slot_number > self.capacity or slot_number <= 0:
            raise InvalidSlotException()

        all_slots: dict[int: Slot] = self.slots
        if slot_number not in all_slots:
            all_slots[slot_number] = Slot(slot_number)

        return all_slots.get(slot_number)

    def park(self, car: Car, slot_number: int) -> Slot:
        slot: Slot = self.get_slot(slot_number)
        if not slot.is_slot_free():
            raise SlotAlreadyOccupiedException()
        slot.assign_car(car)
        return slot

    def make_slot_free(self, slot_number: int) -> Slot:
        slot: Slot = self.get_slot(slot_number)
        if not slot.is_slot_free():
            slot.un_assign_car()
        return slot
