from src.conditions.PieceMoveFurtherCondition.iPieceMoveFurtherCondition import iPieceMoveFurtherCondition
from src.models.board import Board
from src.models.cell import Cell
from src.models.piece import Piece

'''
Default condition for moving further. By default, a piece is allowed to move from a cell only if the cell was free
when it came there
'''


class PieceMoveFurtherConditionDefault(iPieceMoveFurtherCondition):

    def can_pick_move_further_from_cell(self, piece: Piece, cell: Cell, board: Board) -> bool:
        return cell.is_free()

