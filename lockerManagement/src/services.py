import uuid

from src.exceptions import NoSlotAvailableException
from src.models import LockerItem, LockerUser, DeliveryPerson, Size
from src.repositories import *
from src.strategies import ISlotAssignmentStrategy, ISlotFilteringStrategy, IOtpGenerator


# Locker Service
class LockerService:
    def __init__(self, assignment_strategy: ISlotAssignmentStrategy,
                 locker_repository: ILockerRepository, slot_filtering_strategy: ISlotFilteringStrategy):
        self.assignment_strategy: ISlotAssignmentStrategy = assignment_strategy
        self.locker_repository: ILockerRepository = locker_repository
        self.slot_filtering_strategy: ISlotFilteringStrategy = slot_filtering_strategy

    def create_locker(self, locker_id: str) -> Locker:
        return self.locker_repository.create_locker(locker_id)

    def create_slot(self, locker: Locker, slot_size: Size) -> Slot:
        slot: Slot = Slot(uuid.uuid4().hex, slot_size, locker)
        locker.add_slot(slot)
        return slot

    def get_all_available_slots(self) -> list[Slot]:
        return self.locker_repository.get_all_available_slots()

    def allocate_slot(self, locker_item: LockerItem):
        all_available_slots: list[Slot] = self.locker_repository.get_all_available_slots()
        filtered_slots: list[Slot] = self.slot_filtering_strategy.filter_slots(all_available_slots, locker_item)
        slot_to_be_allocated: Slot = self.assignment_strategy.pick_slot(filtered_slots)

        if slot_to_be_allocated is None:
            raise NoSlotAvailableException()

        slot_to_be_allocated.allocated_package(locker_item)
        return slot_to_be_allocated

    def deallocate_slot(self, slot: Slot):
        slot.deallocate_slot()


# OTP Service
class OtpService:
    def __init__(self, otp_generator: IOtpGenerator, slot_repository: ISlotOtpRepository):
        self.otp_generator: IOtpGenerator = otp_generator
        self.slot_repository: ISlotOtpRepository = slot_repository

    def generate_otp(self, slot: Slot) -> str:
        otp: str = self.otp_generator.generate_otp()
        self.slot_repository.add_otp(otp, slot.slot_id)
        return otp

    def validate_otp(self, slot: Slot, otp: str) -> bool:
        saved_otp: str = self.slot_repository.get_otp(slot.slot_id)
        print(f"saved otp: {saved_otp}")
        if saved_otp is None:
            return False
        if saved_otp != otp:
            return False
        return True


# Notification Service
class NotificationService:

    def notify_user(self, user: LockerUser, otp: str, slot: Slot):
        print(f"Sending notification of otp: {otp} to {user} for slot: {slot}")
        return f"Sending notification of otp: {otp} to {user} for slot: {slot}"


# Delivery person Service
class DeliveryPersonService:
    def get_delivery_person(self, slot: Slot) -> DeliveryPerson:
        # TODO: add some stratrgy to pick delivery person
        return None
