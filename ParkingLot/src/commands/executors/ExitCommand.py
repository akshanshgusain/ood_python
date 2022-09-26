from src.OutputPrinter import OutputPrinter
from src.commands.executors.CommandExecutor import CommandExecutor
from src.models.Command import Command
from src.services.ParkingLotService import ParkingLotService


class ExitCommandExecutor(CommandExecutor):
    COMMAND_NAME: str = "exit"

    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        super().__init__(parking_lot_service, output_printer)

    def validate(self, command: Command) -> bool:
        return len(command.params) != 0

    def execute(self, command: Command):
        self.output_printer.end()
