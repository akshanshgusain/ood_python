from src.exception.StorageFullException import StorageFullException
from src.policy.iEvictionPolicy import iEvictionPolicy
from src.storage.iStorage import iStorage


class CacheProvider:

    def __init__(self, eviction_policy: iEvictionPolicy, storage: iStorage):
        self.eviction_policy: iEvictionPolicy = eviction_policy
        self.storage: iStorage = storage

    def set(self, key, value):
        try:
            self.storage.add(key, value)
            self.eviction_policy.key_accessed(key)
        except StorageFullException as e:
            key_to_remove = self.eviction_policy.evict_key()
            if not key_to_remove:
                raise Exception("Unexpected state")

            self.storage.remove(key_to_remove)
            self.set(key, value)

    def get(self, key):
        value = self.storage.get(key)
        self.eviction_policy.key_accessed(key)
        return value

    def get_current_usage(self) -> float:
        return self.storage.get_current_usage()
