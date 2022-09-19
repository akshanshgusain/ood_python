from abc import ABC, abstractmethod

from src.model.ReadResponse import ReadResponse
from src.model.WriteResponse import WriteResponse


class iLevelCache(ABC):

    @abstractmethod
    def set(self, key, value) -> WriteResponse:
        pass

    @abstractmethod
    def get(self, key) -> ReadResponse:
        pass

    @abstractmethod
    def get_usages(self) -> list[float]:
        pass
