from src.OutputPrinter import OutputPrinter
from src.models.Command import Command
from src.modes.Mode import Mode


class InteractiveMode(Mode):
    def __init__(self, command_executor_factory: CommandExecutorFactory,
                 output_printer: OutputPrinter):
        super().__init__(command_executor_factory, output_printer)

    def process(self):
        self.output_printer.welcome()
        while True:
            ip = input()
            command: Command = Command(ip)
            self.process_command(command)
            if command.command_name == ExitCommandExecutor.COMMAND_NAME:
                break
