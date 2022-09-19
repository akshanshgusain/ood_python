from src.services.BookingService import BookingService
from src.services.PaymentsSerivce import PaymentsService


class PaymentsController:
    def __init__(self, payments_service: PaymentsService, booking_service: BookingService):
        self.payments_service: PaymentsService = payments_service
        self.booking_service: BookingService = booking_service

    def payment_failed(self, booking_id: str, user: str):
        self.payments_service.process_payment_failure(self.booking_service.get_booking(booking_id), user)

    def payment_success(self, booking_id: str, user:str):
        self.booking_service.confirm_booking(self.booking_service.get_booking(booking_id), user)
