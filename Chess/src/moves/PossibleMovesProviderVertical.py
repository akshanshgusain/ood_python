from src.models.board import Board
from src.models.cell import Cell
from src.models.piece import Piece
from src.models.player import Player
from src.moves.PossibleMovesProvider import PossibleMovesProvider
from src.moves.VerticalMoveDirection import VerticalMoveDirection


class PossibleMovesProviderVertical(PossibleMovesProvider):

    def __init__(self, max_steps: int, base_condition: MoveBaseCondition, move_further_condition: MoveFurtherCondition,
                 base_blocker: PieceCellOccupyBlocker, vertical_move_direction: VerticalMoveDirection):
        super().__init__(max_steps, base_condition, move_further_condition, base_blocker)
        self.vertical_move_direction: VerticalMoveDirection = vertical_move_direction

    def possible_moves_as_per_current_type(self,
                                           piece: Piece,
                                           board: Board,
                                           additional_blockers: list[PieceCellOccupyBlocker],
                                           player: Player) -> list[Cell]:
        result: list[Cell] = []
        if self.vertical_move_direction == VerticalMoveDirection.UP or self.vertical_move_direction == VerticalMoveDirection.BOTH:
            result.insert(self.find_all_next_moves(piece, board.get_up_cell, board, additional_blockers, player))
        if self.vertical_move_direction == VerticalMoveDirection.DOWN or self.vertical_move_direction == VerticalMoveDirection.BOTH:
            result.insert(self.find_all_next_moves(piece, board.get_down_cell, board, additional_blockers, player))

        return result
