from src.models.Car import Car


class Slot:
    def __init__(self, slot_number: int):
        self.slot_number: int = slot_number
        self.parked_car: Car = None

    def is_slot_free(self) -> bool:
        return self.parked_car is None

    def assign_car(self, car: Car):
        self.parked_car = car

    def un_assign_car(self):
        self.parked_car = None
