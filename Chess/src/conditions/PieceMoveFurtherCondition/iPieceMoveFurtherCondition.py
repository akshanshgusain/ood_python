from abc import ABC, abstractmethod

from src.models.board import Board
from src.models.cell import Cell
from src.models.piece import Piece


class iPieceMoveFurtherCondition(ABC):

    @abstractmethod
    def can_pick_move_further_from_cell(self, piece: Piece, cell: Cell, board: Board) -> bool:
        pass
