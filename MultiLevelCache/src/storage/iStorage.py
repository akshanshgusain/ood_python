from abc import ABC, abstractmethod


class iStorage(ABC):

    @abstractmethod
    def add(self, key, value):
        pass

    @abstractmethod
    def remove(self, key):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def get_current_usage(self) -> float:
        pass
