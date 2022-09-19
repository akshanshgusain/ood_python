from src.model.LevelCacheData import LevelCacheData
from src.model.ReadResponse import ReadResponse
from src.model.WriteResponse import WriteResponse
from src.provider.CacheProvider import CacheProvider
from src.provider.iLevelCache import iLevelCache


class DefaultLevelCache(iLevelCache):

    def __init__(self, level_cache_data: LevelCacheData,
                 cache_provider: CacheProvider,
                 next_level: iLevelCache):
        self.level_cache_data: LevelCacheData = level_cache_data
        self.cache_provider: CacheProvider = cache_provider
        self.next_level: iLevelCache = next_level

    def set(self, key, value) -> WriteResponse:
        cur_time: float = 0
        cur_level_value = self.cache_provider.get(key)
        cur_time += self.level_cache_data.read_time
        if value != cur_level_value:
            self.cache_provider.set(key, value)
            cur_time += self.level_cache_data.write_time
        cur_time += self.next_level.set(key, value).time_taken
        return WriteResponse(cur_time)

    def get(self, key) -> ReadResponse:
        cur_time = 0.0
        cur_level_value = self.cache_provider.get(key)
        cur_time += self.level_cache_data.read_time

        # L1 -> L2 -> L3 Recursion
        if cur_level_value is None:
            next_response: ReadResponse = self.next_level.get(key)
            cur_time += next_response.total_time
            cur_level_value = next_response.value
            if cur_level_value is not None:
                self.cache_provider.set(key, cur_level_value)
                cur_time += self.level_cache_data.write_time

        return ReadResponse(cur_level_value, cur_time)

    def get_usages(self) -> list[float]:
        usages: list[float] = []
        if self.next_level is None:
            usages = []
        else:
            usages = self.next_level.get_usages()

        usages.insert(0, self.cache_provider.get_current_usage())
        return usages
