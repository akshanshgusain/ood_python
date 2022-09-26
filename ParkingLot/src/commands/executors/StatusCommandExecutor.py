from src.OutputPrinter import OutputPrinter
from src.commands.executors.CommandExecutor import CommandExecutor
from src.models.Car import Car
from src.models.Command import Command
from src.models.Slot import Slot
from src.services.ParkingLotService import ParkingLotService


def pad_string(word: str, length: int) -> str:
    new_word: str = word
    for i in range(len(word), length):
        new_word = new_word + " "
    return new_word


class StatusCommandExecutor(CommandExecutor):
    COMMAND_NAME = "status"

    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        super().__init__(parking_lot_service, output_printer)

    def validate(self, command: Command) -> bool:
        return len(command.params) == 0

    def execute(self, command: Command):
        occupied_slots: list[Slot] = self.parking_lot_service.get_occupied_slots()
        if len(occupied_slots) == 0:
            self.output_printer.parkinglot_empty()
            return

        self.output_printer.status_header()
        for slot in occupied_slots:
            parked_car: Car = slot.parked_car
            slot_number: str = str(slot.slot_number)
            self.output_printer.print_message(pad_string(slot_number, 12)
                                              + pad_string(parked_car.registration_number, 19)
                                              + parked_car.color)
