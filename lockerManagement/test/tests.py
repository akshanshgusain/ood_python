import unittest
import uuid

from src.controllers import *
from src.models import Contact, Package
from src.repositories import *
from src.strategies import *


# Utils Functions
def random_string() -> str:
    return uuid.uuid4().hex


def random_otp() -> str:
    return random_string()


def random_email() -> str:
    return random_string() + "@gmail.com"


def random_buyer() -> Buyer:
    return Buyer(Contact(random_string(), random_email()))


def create_test_locker_with_slots(locker_controller: LockerController, num_slots: int, slot_size: Size) -> Locker:
    locker: Locker = locker_controller.create_locker(random_string())
    for i in range(num_slots):
        slot_1: Slot = locker_controller.create_slot(locker, slot_size)
        locker.add_slot(slot_1)
    return locker


def random_locker_item(item_size: Size) -> LockerItem:
    return Package(random_string(), item_size)


class BaseTest(unittest.TestCase):
    locker_controller: LockerController
    order_controller: OrderController
    otp_service: OtpService
    locker_service: LockerService
    notification_service: NotificationService = NotificationService()

    def setUp(self) -> None:
        # Strategies
        random_generator_default: RandomGeneratorDefault = RandomGeneratorDefault()
        locker_assignment_strategy: ISlotAssignmentStrategy = SlotAssignmentStrategy(random_generator_default)
        slot_filtering_strategy: ISlotFilteringStrategy = SlotFilteringStrategySizeBased()
        random_otp_generator: IOtpGenerator = OtpGeneratorRandom(5, random_generator_default)

        # repository
        locker_repository: ILockerRepository = LockerRepositoryInMemory()
        slot_otp_repository: ISlotOtpRepository = SlotOtpRepositoryInMemory()

        # services

        self.locker_service = LockerService(locker_assignment_strategy, locker_repository, slot_filtering_strategy)
        self.otp_service = OtpService(random_otp_generator, slot_otp_repository)

        # controllers
        self.locker_controller = LockerController(self.locker_service, self.otp_service)
        self.order_controller = OrderController(self.locker_service, self.otp_service, self.notification_service)


class OtpVerificationTests(BaseTest):
    def test_otp_works_correctly(self):
        # Arrange
        locker: Locker = create_test_locker_with_slots(self.locker_controller, 2, Size(10, 10))
        buyer: Buyer = random_buyer()
        item: LockerItem = random_locker_item(Size(5, 5))
        otp: str = random_otp()

        # Act
        slot: Slot = self.order_controller.allocate_locker(buyer, item)

        # Assertions
        res: str = self.notification_service.notify_user(buyer, otp, slot)
        self.assertIsNotNone(res)
        self.assertEqual(res, f"Sending notification of otp: {otp} to {buyer} for slot: {slot}")

    def test_invalid_otp_does_not_unlock_slot(self):
        # Arrange
        locker: Locker = create_test_locker_with_slots(self.locker_controller, 2, Size(10, 10))
        buyer: Buyer = random_buyer()
        item: LockerItem = random_locker_item(Size(5, 5))
        otp: str = random_otp()

        # Act
        slot: Slot = self.order_controller.allocate_locker(buyer, item)

        # Assert
        is_success: bool = self.locker_controller.unlock_slot(slot, otp)
        self.assertFalse(is_success)


class SlotAllocationTests(BaseTest):
    def test_slot_allocation_to_user(self):
        locker1: Locker = create_test_locker_with_slots(self.locker_controller, 20, Size(10, 10))
        locker2: Locker = create_test_locker_with_slots(self.locker_controller, 20, Size(5, 5))
        buyer: Buyer = random_buyer()
        item1: LockerItem = random_locker_item(Size(7.5, 5))
        item2: LockerItem = random_locker_item(Size(7.5, 5))

        # Act
        all_slots: list[Slot] = self.locker_controller.get_available_slots()

        slot1: Slot = self.order_controller.allocate_locker(buyer, item1)
        all_available_slots_post_1: list[Slot] = self.locker_controller.get_available_slots()

        slot2: Slot = self.order_controller.allocate_locker(buyer, item2)
        all_available_slots_post_2: list[Slot] = self.locker_controller.get_available_slots()

        # Assertions
        # Slot 1 should be available initially
        self.assertTrue(slot1 in all_slots)
        self.assertFalse(slot1 in all_available_slots_post_1)
        # self.assertFalse(slot1 in all_available_slots_post_2)

        # Slot2 should be available till item 2 is not allotted.
        # self.assertTrue(slot2 in all_slots)
        # self.assertTrue(slot2 in all_available_slots_post_1)
        # self.assertFalse(slot2 in all_available_slots_post_2)

        # After deallocating slot1, it should get available. Slot2 should still be occupied.
        self.locker_controller.deallocate_slot(slot1)
        self.assertTrue(slot1 in self.locker_controller.get_available_slots())
        self.assertFalse(slot2 in self.locker_controller.get_available_slots())

        # After deallocating slot2 also now, both should be available now;
        self.locker_controller.deallocate_slot(slot2)
        self.assertTrue(slot1 in self.locker_controller.get_available_slots())
        self.assertTrue(slot2 in self.locker_controller.get_available_slots())
    