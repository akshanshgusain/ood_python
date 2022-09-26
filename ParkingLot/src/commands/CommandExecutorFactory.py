from src.OutputPrinter import OutputPrinter
from src.commands.executors.ColorToRegNumberCommandExecutor import ColorToRegNumberCommandExecutor
from src.commands.executors.ColorToSlotNumberCommandExecutor import ColorToSlotNumberCommandExecutor
from src.commands.executors.CommandExecutor import CommandExecutor
from src.commands.executors.CreateParkingLotCommandExecutor import CreateParkingLotCommandExecutor
from src.commands.executors.ExitCommand import ExitCommandExecutor
from src.commands.executors.LeaveCommandExecutor import LeaveCommandExecutor
from src.commands.executors.ParkCommandExecutor import ParkCommandExecutor
from src.commands.executors.SlotForRegNumberCommandExecutor import SlotForRegNumberCommandExecutor
from src.commands.executors.StatusCommandExecutor import StatusCommandExecutor
from src.exceptions.InvalidCommandException import InvalidCommandException
from src.models.Command import Command
from src.services.ParkingLotService import ParkingLotService


class CommandExecutorFactory:
    def __init__(self, parking_lot_service: ParkingLotService,
                 output_printer: OutputPrinter):
        self.commands: dict[str: CommandExecutor] = {
            CreateParkingLotCommandExecutor.COMMAND_NAME: CreateParkingLotCommandExecutor(parking_lot_service,
                                                                                          output_printer),
            ParkCommandExecutor.COMMAND_NAME: ParkCommandExecutor(parking_lot_service, output_printer),
            LeaveCommandExecutor.COMMAND_NAME: LeaveCommandExecutor(parking_lot_service, output_printer),
            StatusCommandExecutor.COMMAND_NAME: StatusCommandExecutor(parking_lot_service, output_printer),
            ColorToRegNumberCommandExecutor.COMMAND_NAME: ColorToRegNumberCommandExecutor(parking_lot_service,
                                                                                          output_printer),

            SlotForRegNumberCommandExecutor.COMMAND_NAME: SlotForRegNumberCommandExecutor(parking_lot_service,
                                                                                          output_printer),
            ExitCommandExecutor.COMMAND_NAME: ExitCommandExecutor(parking_lot_service, output_printer),
            ColorToSlotNumberCommandExecutor.COMMAND_NAME: ColorToSlotNumberCommandExecutor(parking_lot_service,
                                                                                            output_printer),
        }

    def get_command_executor(self, command: Command) -> CommandExecutor:
        command_executor: CommandExecutor = self.commands[command.command_name]
        if command_executor is None:
            raise InvalidCommandException()
        return command_executor
