import unittest

from src.OutputPrinter import OutputPrinter
from src.commands.CommandExecutorFactory import CommandExecutorFactory
from src.commands.executors.ColorToRegNumberCommandExecutor import ColorToRegNumberCommandExecutor
from src.commands.executors.CreateParkingLotCommandExecutor import CreateParkingLotCommandExecutor
from src.models.Command import Command
from src.services.ParkingLotService import ParkingLotService


class CreateParkingLotCommandExecutorTest(unittest.TestCase):
    parking_lot_service: ParkingLotService
    output_printer: OutputPrinter
    color_to_reg_number_command_executor: ColorToRegNumberCommandExecutor
    create_parking_lot_executor: CreateParkingLotCommandExecutor

    def setUp(self) -> None:
        self.parking_lot_service = ParkingLotService()
        self.output_printer = OutputPrinter()
        self.color_to_reg_number_command_executor = ColorToRegNumberCommandExecutor(self.parking_lot_service,
                                                                                    self.output_printer)
        self.create_parking_lot_executor = CreateParkingLotCommandExecutor(self.parking_lot_service,
                                                                           self.output_printer)

    def test_valid_command(self):
        self.assertTrue(self.color_to_reg_number_command_executor.validate(
            Command("registration_numbers_for_cars_with_colour red")))

    def test_invalid_commands(self):
        self.assertFalse(self.color_to_reg_number_command_executor.validate(
            Command("registration_numbers_for_cars_with_colour")))
        self.assertFalse(self.color_to_reg_number_command_executor.validate(
            Command("registration_numbers_for_cars_with_colour red honda")))

    def test_when_no_cars_found_with_a_color(self):
        self.create_parking_lot_executor.execute(Command("create_parking_lot 6"))
        self.assertEqual(
            self.color_to_reg_number_command_executor.execute(Command("registration_numbers_for_cars_with_colour red")),
            self.output_printer.not_found())
