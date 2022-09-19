
class ReadResponse:
    def __init__(self, value, total_time: float):
        self.value = value  # Generic
        self.total_time: float = total_time
