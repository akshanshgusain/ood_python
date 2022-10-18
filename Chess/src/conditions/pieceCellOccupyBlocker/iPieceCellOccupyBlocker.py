from abc import ABC, abstractmethod

from src.models.models import Cell, Piece, Board, Player

'''This check tells whether a piece can occupy a given cell in the board or not.'''


class iPieceCellOccupyBlocker(ABC):

    @abstractmethod
    def is_cell_non_occupiable_for_piece(self, cell: Cell, piece: Piece, board: Board, player: Player) -> bool:
        pass
