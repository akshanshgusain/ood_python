from abc import ABC, abstractmethod

from src.exceptions import LockerAlreadyExistsException
from src.models import Locker, Slot


class ILockerRepository(ABC):
    @abstractmethod
    def create_locker(self, id: str) -> Locker:
        pass

    @abstractmethod
    def get_all_available_slots(self) -> list[Slot]:
        pass


class LockerRepositoryInMemory(ILockerRepository):

    def __init__(self):
        self.all_lockers: list[Locker] = []

    def create_locker(self, id: str) -> Locker:
        if self.get_locker(id) is not None:
            raise LockerAlreadyExistsException()
        new_locker: Locker = Locker(id)
        self.all_lockers.append(new_locker)
        return new_locker

    def get_all_available_slots(self) -> list[Slot]:
        available_lockers: list[Slot] = []
        # print("All Slots")
        # for locker in self.all_lockers:
        #     print(locker.get_available_slots())
        #     print("\n")
        # print("----")
        # print("\n\n")
        for locker in self.all_lockers:
            available_lockers.extend(locker.get_available_slots())
        return available_lockers

    def get_locker(self, id: str) -> Locker:
        for locker in self.all_lockers:
            if locker.id == id:
                return locker


class ISlotOtpRepository(ABC):
    @abstractmethod
    def add_otp(self, otp: str, slot_id: str):
        pass

    @abstractmethod
    def get_otp(self, slot_id: str) -> str:
        pass


class SlotOtpRepositoryInMemory(ISlotOtpRepository):
    # Keeping it separate and not in slot object itself as it can be a separate service to handle otps.
    # TODO: Create separate OTP model class may be when use cases increase like handling expiry of otps.

    def __init__(self):
        self.slot_id_to_otp: dict[str: str] = {}

    def add_otp(self, otp: str, slot_id: str):
        self.slot_id_to_otp[slot_id] = otp

    def get_otp(self, slot_id: str) -> str:
        return self.slot_id_to_otp.get(slot_id)
