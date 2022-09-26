from src.OutputPrinter import OutputPrinter
from src.commands.executors.CommandExecutor import CommandExecutor
from src.models.Command import Command
from src.models.ParkingLot import ParkingLot
from src.services.ParkingLotService import ParkingLotService
from src.strategies.NaturalParkingStrategy import NaturalParkingStrategy


class CreateParkingLotCommandExecutor(CommandExecutor):
    COMMAND_NAME = "create_parking_lot"

    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        super().__init__(parking_lot_service, output_printer)

    def validate(self, command: Command) -> bool:
        if len(command.params) != 1:
            return False
        return command.params[0].isdigit()

    def execute(self, command: Command):
        parking_lot_capacity: int = int(command.params[0])
        parking_lot: ParkingLot = ParkingLot(parking_lot_capacity)
        self.parking_lot_service.create_parking_lot(parking_lot, NaturalParkingStrategy())
        self.output_printer.print_message(f"Created a parking lot with {parking_lot.capacity} slots")
