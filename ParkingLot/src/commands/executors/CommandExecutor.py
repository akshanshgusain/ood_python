from abc import ABC, abstractmethod

from src.OutputPrinter import OutputPrinter
from src.models.Command import Command
from src.services.ParkingLotService import ParkingLotService


class CommandExecutor(ABC):
    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        self.parking_lot_service: ParkingLotService = parking_lot_service
        self.output_printer: OutputPrinter = output_printer

    @abstractmethod
    def validate(self, command: Command) -> bool:
        pass

    @abstractmethod
    def execute(self, command: Command):
        pass
