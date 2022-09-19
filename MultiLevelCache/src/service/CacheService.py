from src.model.ReadResponse import ReadResponse
from src.model.StatsResponse import StatsResponse
from src.model.WriteResponse import WriteResponse
from src.provider.iLevelCache import iLevelCache


class CacheService:

    def __init__(self, multi_level_cache: iLevelCache, last_count: int):
        self.multi_level_cache: iLevelCache = multi_level_cache
        self.last_read_times: list[float] = []
        self.last_write_times: list[float] = []
        self.last_count: int = last_count

    def set(self, key, value) -> WriteResponse:
        write_response: WriteResponse = self.multi_level_cache.set(key, value)
        self.add_times(self.last_write_times, write_response.time_taken)
        return write_response

    def get(self, key) -> ReadResponse:
        read_response: ReadResponse = self.multi_level_cache.get(key)
        self.add_times(self.last_read_times, read_response.total_time)
        return read_response

    def stats(self) -> StatsResponse:
        return StatsResponse(self.get_avg_read_time(),
                             self.get_avg_write_time(),
                             self.multi_level_cache.get_usages())

    def get_avg_read_time(self) -> float:
        return sum(self.last_read_times) / len(self.last_read_times)

    def get_avg_write_time(self) -> float:
        return sum(self.last_write_times) / len(self.last_write_times)

    def add_times(self, times: list[float], time: float):
        if len(times) == self.last_count:
            del times[0]
        times.append(time)
