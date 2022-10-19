import unittest

from src.provider.CacheProvider import CacheProvider
from src.service.CacheService import CacheService


class CacheTest(unittest.TestCase):
    cache: CacheService = None

    def setUp(self) -> None:
        self.cache = CacheProvider.default_cache(3)

    def test_case_01(self):
        self.cache.put(1, 1)
        self.cache.put(2, 2)

        self.assertEqual(1, self.cache.get(1))
        self.cache.put(3, 3)
        self.assertEqual(3, self.cache.get(3))

        self.cache.put(4, 4)
        self.cache.get(2)  # This should throw exception "Tried to access non-existing key."
