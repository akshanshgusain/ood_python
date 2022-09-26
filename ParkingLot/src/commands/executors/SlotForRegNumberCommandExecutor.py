from src.OutputPrinter import OutputPrinter
from src.commands.executors.CommandExecutor import CommandExecutor
from src.models.Command import Command
from src.models.Slot import Slot
from src.services.ParkingLotService import ParkingLotService


class SlotForRegNumberCommandExecutor(CommandExecutor):
    COMMAND_NAME = "slot_number_for_registration_number"

    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        super().__init__(parking_lot_service, output_printer)

    def validate(self, command: Command) -> bool:
        return len(command.params) == 1

    def execute(self, command: Command):
        occupied_slots: list[Slot] = self.parking_lot_service.get_occupied_slots()
        reg_number_to_find = command.params[0]
        found_slots: list[Slot] = []
        for slot in occupied_slots:
            if slot.parked_car.registration_number == reg_number_to_find:
                found_slots.append(slot)
        if len(found_slots) != 0:
            self.output_printer.print_message(found_slots[0].slot_number)
        else:
            self.output_printer.not_found()
