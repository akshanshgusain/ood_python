from src.models.board import Board
from src.models.cell import Cell
from src.models.piece import Piece
from src.models.player import Player
from src.moves.PossibleMovesProvider import PossibleMovesProvider


class PossibleMovesProviderDiagonal(PossibleMovesProvider):
    def __init__(self,
                 max_steps: int,
                 base_condition: MoveBaseCondition,
                 move_further_condition: MoveFurtherCondition,
                 base_blocker: PieceCellOccupyBlocker):
        super().__init__(max_steps, base_condition, move_further_condition, base_blocker)

    def possible_moves_as_per_current_type(self,
                                           piece: Piece,
                                           board: Board,
                                           additional_blockers: list[PieceCellOccupyBlocker],
                                           player: Player) -> list[Cell]:
        return None
