from abc import ABC, abstractmethod

from src.OutputPrinter import OutputPrinter
from src.commands.executors.CommandExecutor import CommandExecutor
from src.exceptions.InvalidCommandException import InvalidCommandException
from src.models.Command import Command


class Mode(ABC):
    def __init__(self, command_executor_factory: CommandExecutorFactory,
                 output_printer: OutputPrinter):
        self.command_executor_factory: CommandExecutorFactory = command_executor_factory
        self.output_printer: OutputPrinter = output_printer

    def process_command(self, command: Command):
        command_executor: CommandExecutor = self.command_executor_factory.get_command_executor(command)
        if command_executor.validate(command):
            command_executor.execute(command)
        else:
            raise InvalidCommandException()

    # Abstract method to process the mode. Each mode will process in its own way.
    @abstractmethod
    def process(self):
        pass
