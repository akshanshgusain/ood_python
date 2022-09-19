import unittest

from src.model.LevelCacheData import LevelCacheData
from src.model.ReadResponse import ReadResponse
from src.model.WriteResponse import WriteResponse
from src.policy.LRUEvictionPolicy import LRUEvictionPolicy
from src.provider.CacheProvider import CacheProvider
from src.provider.DefaultLevelCache import DefaultLevelCache
from src.provider.NullEffectLevelCache import NullEffectLevelCache
from src.service.CacheService import CacheService
from src.storage.InMemoryStorage import InMemoryStorage


class BaseTest(unittest.TestCase):
    def test_case_1(self):
        c1: CacheProvider = self.create_cache(10)
        c2: CacheProvider = self.create_cache(20)

        level_cache_data_1: LevelCacheData = LevelCacheData(1, 3)
        level_cache_data_2: LevelCacheData = LevelCacheData(2, 4)

        l2_cache: DefaultLevelCache = DefaultLevelCache(level_cache_data_2, c2, NullEffectLevelCache())
        l1_cache: DefaultLevelCache = DefaultLevelCache(level_cache_data_1, c1, l2_cache)

        cache_service: CacheService = CacheService(l1_cache, 5)

        w1: WriteResponse = cache_service.set("k1", "v1")
        w2: WriteResponse = cache_service.set("k2", "v2")

        self.assertEqual(10, w1.time_taken)
        self.assertEqual(10, w2.time_taken)

        r1: ReadResponse = cache_service.get("k1")
        self.assertEqual("v1", r1.value)
        self.assertEqual(1, r1.total_time)

        r1: ReadResponse = cache_service.get("k2")
        self.assertEqual("v2", r1.value)
        self.assertEqual(1, r1.total_time)

        # Explicitly remove key from l1 for testing.
        c1.set("k1", None)

        r1_after_removal_from_l1: ReadResponse = cache_service.get("k1")
        self.assertEqual("v1", r1_after_removal_from_l1.value)
        self.assertEqual(6, r1_after_removal_from_l1.total_time)

        re_read: ReadResponse = cache_service.get("k1")
        self.assertEqual("v1", re_read.value)
        self.assertEqual(1, re_read.total_time)

        re_write_response: WriteResponse = cache_service.set("k1", "v1")
        self.assertEqual(3, re_write_response.time_taken)

    @classmethod
    def create_cache(cls, capacity: int) -> CacheProvider:
        return CacheProvider(
            LRUEvictionPolicy(),
            InMemoryStorage(capacity)
        )
