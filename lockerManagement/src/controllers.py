from src.models import Locker, Size, Slot, Buyer, LockerItem, DeliveryPerson
from src.services import LockerService, OtpService, NotificationService, DeliveryPersonService


# Locker Controller
class LockerController:

    def __init__(self, locker_service: LockerService, otp_service: OtpService):
        self.locker_service: LockerService = locker_service
        self.otp_service: OtpService = otp_service


    def create_locker(self, locker_id: str) -> Locker:
        return self.locker_service.create_locker(locker_id)

    def create_slot(self, locker: Locker, slot_size: Size) -> Slot:
        return self.locker_service.create_slot(locker, slot_size)

    def get_available_slots(self) -> list[Slot]:
        return self.locker_service.get_all_available_slots()

    def unlock_slot(self, slot: Slot, otp: str) -> bool:
        return self.otp_service.validate_otp(slot, otp)

    def deallocate_slot(self, slot: Slot):
        self.locker_service.deallocate_slot(slot)


# Order Controller
class OrderController:

    def __init__(self, locker_service: LockerService, otp_service: OtpService,
                 notification_service: NotificationService):
        self.locker_service: LockerService = locker_service
        self.otp_service: OtpService = otp_service
        self.notification_service: NotificationService = notification_service

    def allocate_locker(self, buyer: Buyer, locker_item: LockerItem):
        slot: Slot = self.locker_service.allocate_slot(locker_item)
        otp: str = self.otp_service.generate_otp(slot)
        self.notification_service.notify_user(buyer, otp, slot)
        return slot


# Return Controller
class ReturnController:
    def __init__(self, locker_service: LockerService, otp_service: OtpService,
                 notification_service: NotificationService, delivery_person_service: DeliveryPersonService):
        self.locker_service: LockerService = locker_service
        self.otp_service: OtpService = otp_service
        self.notification_service: NotificationService = notification_service
        self.delivery_person_service: DeliveryPersonService = delivery_person_service

    def allocate_locker(self, buyer: Buyer, locker_item: LockerItem):
        slot: Slot = self.locker_service.allocate_slot(locker_item)
        otp: str = self.otp_service.generate_otp(slot)
        delivery_person_service: DeliveryPerson = self.delivery_person_service.get_delivery_person(slot)
        self.notification_service.notify_user(buyer, otp, slot)
