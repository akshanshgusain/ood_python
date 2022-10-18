from abc import ABC, abstractmethod

from src.models.board import Board
from src.models.cell import Cell
from src.models.piece import Piece
from src.models.player import Player

'''
Provider class which returns all the possible cells for a given type of moves. For example, horizontal type of move
will give all the cells which can be reached by making only horizontal moves.
'''


class PossibleMovesProvider(ABC):
    def __init__(self,
                 max_steps: int,
                 base_condition: MoveBaseCondition,
                 move_further_condition: PieceMoveFurtherCondition,
                 base_blocker: PieceCellOccupyBlocker,
                 ):
        self.max_steps: int = max_steps
        self.base_condition: MoveBaseCondition = base_condition
        self.move_further_condition: PieceMoveFurtherCondition = move_further_condition
        self.base_blocker: PieceCellOccupyBlocker = base_blocker

    # Public method which actually gives all possible cells which can be reached via current type of move.

    def possible_moves(self, piece: Piece, in_board: Board, additional_blockers: list[PieceCellOccupyBlocker],
                       player: Player) -> list[Cell]:
        if self.base_condition.is_base_condition_fullfilled(piece):
            return self.possible_moves_as_per_current_type(piece, in_board, additional_blockers, player)
        return None

    '''Abstract method which needs to be implemented by each type of move to give possible moves as per their 
    behaviour. '''

    @abstractmethod
    def possible_moves_as_per_current_type(self, piece: Piece, board: Board,
                                           additional_blockers: list[PieceCellOccupyBlocker], player: Player) -> list[
        Cell]:
        pass

    # Helper method used by all the subtypes to create the list of cells which can be reached.
    def find_all_next_moves(self, piece: Piece, next_cell_provider: NextCellProvider, board: Board,
                            cell_occupy_blockers: list[PieceCellOccupyBlocker], player: Player) -> list[Cell]:
        result: list[Cell] = []
        next_cell: Cell = next_cell_provider.next_cell(piece.current_cell)
        num_steps: int = 1
        while next_cell is not None and num_steps <= self.max_steps:
            if self.check_if_cell_be_occupied(piece, next_cell, board, cell_occupy_blockers, player):
                result.append(next_cell)
            if self.move_further_condition.can_piece_move_further_from_cell(piece, next_cell, board):
                break
            next_cell = next_cell_provider.next_cell(next_cell)
            num_steps += 1

        return result

    '''
    Helper method which checks if a given cell can be occupied by the piece or not. It makes use of list of
    PieceCellOccupyBlocker passed to it while checking. Also each move has one base blocker which it should
    also check.
    '''

    def check_if_cell_can_be_occupied(self, piece: Piece, cell: Cell, board: Board,
                                      additional_blockers: list[PieceCellOccupyBlocker],
                                      player: Player) -> bool:
        if self.base_blocker is not None and self.base_blocker.is_cell_not_occupied_for_piece(cell, piece, board,
                                                                                              player):
            return False
        for cell_occupy_blocker in additional_blockers:
            if cell_occupy_blocker.is_cell_not_occupied_for_piece(cell, piece, board, player):
                return False
        return True
