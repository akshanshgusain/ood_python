from src.OutputPrinter import OutputPrinter
from src.commands.executors.CommandExecutor import CommandExecutor
from src.models.Command import Command
from src.services.ParkingLotService import ParkingLotService


class LeaveCommandExecutor(CommandExecutor):
    COMMAND_NAME = "leave"

    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        super().__init__(parking_lot_service, output_printer)

    def validate(self, command: Command) -> bool:
        if len(command.params) != 1:
            return False
        return command.params[0].isdigit()

    def execute(self, command: Command):
        slot: int = int(command.params[0])
        self.parking_lot_service.make_slot_empty(slot)
        self.output_printer.print_message(f"Slot number {slot} is vacant now")

