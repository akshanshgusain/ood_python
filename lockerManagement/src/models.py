from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from src.exceptions import SlotAlreadyOccupiedException


# ''' do not directly initialise Locker User'''
class LockerUser(ABC):
    def __init__(self, contact: Contact):
        self.contact: Contact = contact


class Contact:
    def __init__(self, phone: str, email: str):
        self.phone: str = phone
        self.email: str = email


class Buyer(LockerUser):
    def __init__(self, contact: Contact):
        super().__init__(contact)


class DeliveryPerson(LockerUser):
    def __init__(self, contact: Contact):
        super().__init__(contact)


class Locker:
    def __init__(self, id: str):
        self.id: str = id
        self.slots: list[Slot] = []

    def add_slot(self, new_slot: Slot):
        self.slots.append(new_slot)

    def get_available_slots(self) -> list[Slot]:
        available_slots: list[Slot] = []
        for slot in self.slots:
            if slot.is_available:
                available_slots.append(slot)
        return available_slots


class Size:
    def __init__(self, width: float, height: float):
        self.width: float = width
        self.height: float = height

    def can_accommodate(self, size_to_accommodate: Size) -> bool:
        return self.width >= size_to_accommodate.width and self.height >= size_to_accommodate.height


class LockerItem(ABC):
    @abstractmethod
    def get_size(self) -> Size:
        pass


class Package(LockerItem):
    def __init__(self, id: str, size: Size):
        self.id: str = id
        self.size: Size = size

    def get_size(self) -> Size:
        return self.size


class Slot:
    def __init__(self, slot_id: str, size: Size, locker: Locker):
        self.slot_id: str = slot_id
        self.size: Size = size
        self.locker: Locker = locker
        self.currentLockerItem: LockerItem = None
        self.allocation_date: datetime = None

    def allocated_package(self, new_locker_item: LockerItem):
        if self.currentLockerItem is not None:
            raise SlotAlreadyOccupiedException()
        self.allocation_date = datetime.now()
        self.currentLockerItem = new_locker_item

    def deallocate_slot(self):
        self.currentLockerItem = None

    def is_available(self) -> bool:
        return self.locker is None
