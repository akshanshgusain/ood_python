from src.OutputPrinter import OutputPrinter
from src.models.Command import Command
from src.modes.Mode import Mode


class FileMode(Mode):

    def __init__(self,
                 command_executor_factory: CommandExecutorFactory,
                 output_printer: OutputPrinter,
                 file_name: str):
        super().__init__(command_executor_factory, output_printer)
        self.file_name: str = file_name

    def process(self):
        file = open(self.file_name, 'r')
        for line in file:
            command: Command = Command(line)
            self.process_command(command)

