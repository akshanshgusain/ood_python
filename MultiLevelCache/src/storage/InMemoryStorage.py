from src.exception.StorageFullException import StorageFullException
from src.storage.iStorage import iStorage


class InMemoryStorage(iStorage):

    def __init__(self, capacity: int):
        self.storage = {}  # Generic
        self.capacity: int = capacity

    def add(self, key, value):
        if self.is_storage_full():
            raise StorageFullException()
        self.storage[key] = value

    def remove(self, key):
        self.storage.pop(key)

    def get(self, key):
        return self.storage.get(key)

    def get_current_usage(self) -> float:
        return len(self.storage) / self.capacity

    def is_storage_full(self):
        return len(self.storage) == self.capacity
