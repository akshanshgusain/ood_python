from iStorage import iStorage
from src.exceptions.NotFoundException import NotFoundException
from src.exceptions.StorageFullException import StorageFullException


class HashMapBasedStorage(iStorage):
    def __init__(self, capacity: int):
        self.storage: dict = {}
        self.capacity: int = capacity

    def add(self, key, value):
        if self.is_storage_full():
            raise StorageFullException()
        self.storage[key] = value

    def remove(self, key):
        if key not in self.storage:
            raise NotFoundException()
        self.storage.pop(key)

    def get(self, key):
        if key not in self.storage:
            raise NotFoundException()
        return self.storage.get(key)

    def is_storage_full(self) -> bool:
        return len(self.storage) == self.capacity
