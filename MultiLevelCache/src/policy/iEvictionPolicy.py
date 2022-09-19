from abc import ABC, abstractmethod


class iEvictionPolicy(ABC):

    @abstractmethod
    def key_accessed(self, key):
        pass

    @abstractmethod
    def evict_key(self):
        pass
