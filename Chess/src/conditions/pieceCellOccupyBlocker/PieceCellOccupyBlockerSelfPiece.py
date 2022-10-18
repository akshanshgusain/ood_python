from src.conditions.pieceCellOccupyBlocker.iPieceCellOccupyBlocker import iPieceCellOccupyBlocker
from src.models.board import Board
from src.models.cell import Cell
from src.models.piece import Piece
from src.models.player import Player


class PieceCellOccupyBlockerSelfPiece(iPieceCellOccupyBlocker):

    def is_cell_non_occupiable_for_piece(self, cell: Cell, piece: Piece, board: Board, player: Player) -> bool:
        if cell.is_free():
            return False
        return cell.current_piece.color == piece.color
