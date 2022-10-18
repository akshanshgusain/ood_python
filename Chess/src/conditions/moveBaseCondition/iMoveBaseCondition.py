from abc import ABC, abstractmethod

from src.models.piece import Piece

'''
It provides the base condition for a piece to make a move. The piece would only be allowed to move from its current
position if the condition fulfills.
'''


class iMoveBaseCondition(ABC):

    @abstractmethod
    def is_base_condition_fulfilled(self, piece: Piece) -> bool:
        pass
