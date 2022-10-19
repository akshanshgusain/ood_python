from src.policies.LRUEvictionPolicy import LRUEvictionPolicy
from src.policies.iEvectionPolicy import iEvectionPolicy
from src.service.CacheService import CacheService
from src.storage.HashMapBasedStorage import HashMapBasedStorage
from src.storage.iStorage import iStorage


class CacheProvider:
    @classmethod
    def default_cache(cls, capacity: int) -> CacheService:
        return CacheService(LRUEvictionPolicy(), HashMapBasedStorage(capacity))
