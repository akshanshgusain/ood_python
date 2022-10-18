from src.conditions.moveBaseCondition.iMoveBaseCondition import iMoveBaseCondition
from src.models.piece import Piece

'''This condition allows a move only if cell is making a move from its initial position. That is first move ever.'''


class MoveBaseConditionFirstMove(iMoveBaseCondition):
    def is_base_condition_fulfilled(self, piece: Piece) -> bool:
        return piece.num_moves == 0
