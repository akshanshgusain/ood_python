from src.OutputPrinter import OutputPrinter
from src.commands.executors.CommandExecutor import CommandExecutor
from src.exceptions.NoFreeSlotAvailableException import NoFreeSlotAvailableException
from src.models.Car import Car
from src.models.Command import Command
from src.services.ParkingLotService import ParkingLotService


class ParkCommandExecutor(CommandExecutor):
    COMMAND_NAME = "park"

    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        super().__init__(parking_lot_service, output_printer)

    def validate(self, command: Command) -> bool:
        return len(command.params) == 2

    def execute(self, command: Command):
        car: Car = Car(command.params[0], command.params[1])
        try:
            slot: int = self.parking_lot_service.park(car)
            self.output_printer.print_message(f"Allocated slot Number: {slot}")
        except NoFreeSlotAvailableException as exception:
            self.output_printer.parkinglot_full()
