from abc import ABC, abstractmethod

from src.models.cell import Cell


class iNextCellProvider(ABC):

    @abstractmethod
    def next_cell(self, cell: Cell) -> Cell:
        pass
