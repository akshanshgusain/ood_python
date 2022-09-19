from src.model.ReadResponse import ReadResponse
from src.model.WriteResponse import WriteResponse
from src.provider.iLevelCache import iLevelCache


class NullEffectLevelCache(iLevelCache):

    def set(self, key, value) -> WriteResponse:
        return WriteResponse(0.0)

    def get(self, key) -> ReadResponse:
        return ReadResponse(0.0)

    def get_usages(self) -> list[float]:
        return []
