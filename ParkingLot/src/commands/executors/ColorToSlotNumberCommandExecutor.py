from src.OutputPrinter import OutputPrinter
from src.commands.executors.CommandExecutor import CommandExecutor
from src.models.Command import Command
from src.models.Slot import Slot
from src.services.ParkingLotService import ParkingLotService


class ColorToSlotNumberCommandExecutor(CommandExecutor):
    COMMAND_NAME = "slot_numbers_for_cars_with_colour"

    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        super().__init__(parking_lot_service, output_printer)

    def validate(self, command: Command) -> bool:
        return len(command.params) == 1

    def execute(self, command: Command):
        slot_for_color: list[Slot] = self.parking_lot_service.get_slots_for_color(command.params[0])
        if len(slot_for_color) == 0:
            self.output_printer.not_found()
        else:
            result: str = ""
            for slot in slot_for_color:
                result = result + ", " + str(slot.slot_number)
            self.output_printer.print_message(result)

