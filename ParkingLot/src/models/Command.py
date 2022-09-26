from src.exceptions.InvalidCommandException import InvalidCommandException


class Command:
    SPACE: str = " "

    def __init__(self, input_line: str):
        self.input_line: str = input_line

        token_list: list[str] = input_line.strip().split(self.SPACE)
        if len(token_list) == 0:
            raise InvalidCommandException()

        self.command_name = token_list[0].lower()
        token_list.pop(0)

        self.params: list[str] = token_list
