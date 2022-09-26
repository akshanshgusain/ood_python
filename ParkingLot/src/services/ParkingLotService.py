from src.exceptions.ParkingLotException import ParkingLotException
from src.models.Car import Car
from src.models.ParkingLot import ParkingLot
from src.models.Slot import Slot
from src.strategies.iParkingStrategy import iParkingStrategy


class ParkingLotService:
    def __init__(self):
        self.parking_lot: ParkingLot = None
        self.parking_strategy: iParkingStrategy = None

    def create_parking_lot(self, parking_lot: ParkingLot, parking_strategy: iParkingStrategy):
        if self.parking_lot is not None:
            raise ParkingLotException("Parking lot already exists.")
        self.parking_lot = parking_lot
        self.parking_strategy = parking_strategy
        for i in range(1, self.parking_lot.capacity + 1):
            self.parking_strategy.add_slots(i)

    def park(self, car: Car) -> int:
        self.validate_parking_lot_exist()
        next_free_slot: int = self.parking_strategy.get_next_slot()
        self.parking_lot.park(car, next_free_slot)
        self.parking_strategy.remove_slots(next_free_slot)
        return next_free_slot

    def make_slot_free(self, slot_number: int):
        self.validate_parking_lot_exist()
        self.parking_lot.make_slot_free(slot_number)
        self.parking_strategy.add_slots(slot_number)

    def get_occupied_slots(self) -> list[Slot]:
        self.validate_parking_lot_exist()
        occupied_slot_list: list[Slot] = []
        all_slots: dict[int: Slot] = {}
        for i in range(1, self.parking_lot.capacity + 1):
            if i in all_slots:
                slot: Slot = all_slots[i]
                if not slot.is_slot_free():
                    occupied_slot_list.append(slot)
        return occupied_slot_list

    def validate_parking_lot_exist(self):
        if self.parking_lot is None:
            raise ParkingLotException("Parking lot does not exists to park.")

    def get_slots_for_color(self, color: str) -> list[Slot]:
        occupied_slots: list[Slot] = self.get_occupied_slots()
        # occupied_slots_by_color: list[Slot] = []
        return list(filter(lambda slot:  slot.parked_car.color == color, occupied_slots))

        # for slot in occupied_slots:
        #     if slot.parked_car.color == color:
        #         occupied_slots_by_color.append(slot)
        #
        # return occupied_slots_by_color
