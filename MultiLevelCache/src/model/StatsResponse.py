from typing import List


class StatsResponse:
    def __init__(self, avg_read_time: float, avg_write_time: float, usages: List[float]):
        self.avg_read_time: float = avg_read_time
        self.avg_write_time: float = avg_write_time
        self.usages: List[float] = usages
