from src.exceptions.NotFoundException import NotFoundException
from src.exceptions.StorageFullException import StorageFullException
from src.policies.iEvectionPolicy import iEvectionPolicy
from src.storage.iStorage import iStorage


class CacheService:
    def __init__(self, eviction_policy: iEvectionPolicy, storage: iStorage):
        self.eviction_policy: iEvectionPolicy = eviction_policy
        self.storage: iStorage = storage

    def put(self, key, value):
        try:
            self.storage.add(key, value)
            self.eviction_policy.key_accessed(key)
        except StorageFullException as e:
            print("Got storage full. Will try to evict")
            key_to_remove = self.eviction_policy.evict_key()
            if key_to_remove is None:
                raise RuntimeError("Unexpected State. Storage full and no key to evict.")
            self.storage.remove(key_to_remove)
            print(f"Creating space by evicting item... {key_to_remove}")
            self.put(key, value)

    def get(self, key):
        try:
            value = self.storage.get(key)
            self.eviction_policy.key_accessed(key)
            return value
        except NotFoundException as e:
            print("tried to access non-existing key")
            return None
