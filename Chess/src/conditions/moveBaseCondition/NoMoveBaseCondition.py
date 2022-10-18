from src.conditions.moveBaseCondition.iMoveBaseCondition import iMoveBaseCondition
from src.models.piece import Piece


class NoMoveBaseCondition(iMoveBaseCondition):

    def is_base_condition_fulfilled(self, piece: Piece) -> bool:
        return True
