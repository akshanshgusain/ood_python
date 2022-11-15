from __future__ import annotations

import random
from abc import ABC, abstractmethod

from src.models import Slot, LockerItem


# OTP Generator Strategy
class IOtpGenerator(ABC):
    @abstractmethod
    def generate_otp(self):
        pass


class OtpGeneratorRandom(IOtpGenerator):
    def __init__(self, otp_length: int, random_generator: IRandomGenerator):
        self.otp_length: int = otp_length
        self.random_generator: IRandomGenerator = random_generator

    def generate_otp(self) -> str:
        otp = ""
        for i in range(0, self.otp_length):
            otp += str(self.random_generator.get_random_number(10))
        return otp


# RandomGenerator Strategy
class IRandomGenerator(ABC):
    @abstractmethod
    def get_random_number(self, less_than_this: int) -> int:
        pass


class RandomGeneratorDefault(IRandomGenerator):
    def get_random_number(self, less_than_this: int) -> int:
        return random.randint(1, less_than_this)


#  Slot Assignment Strategy
class ISlotAssignmentStrategy(ABC):
    @abstractmethod
    def pick_slot(self, slots: list[Slot]) -> Slot:
        pass


class SlotAssignmentStrategy(ISlotAssignmentStrategy):
    def __init__(self, random_generator: IRandomGenerator):
        self.random_generator: IRandomGenerator = random_generator

    def pick_slot(self, slots: list[Slot]) -> Slot:
        if len(slots) == 0:
            return None
        slot_num: int = self.random_generator.get_random_number(len(slots)-1)
        return slots[slot_num]


# Slot Filtering Strategy
class ISlotFilteringStrategy(ABC):
    @abstractmethod
    def filter_slots(self, slots: list[Slot], locker_item: LockerItem) -> list[Slot]:
        pass


class SlotFilteringStrategySizeBased(ISlotFilteringStrategy):
    def filter_slots(self, slots: list[Slot], locker_item: LockerItem) -> list[Slot]:
        filtered: list[Slot] = []
        for slot in slots:
            if slot.size.can_accommodate(locker_item.get_size()):
                filtered.append(slot)
        # filtered = filter(lambda slot: slot.size.can_accommodate(locker_item.get_size()), slots)
        return list(filtered)
