from __future__ import annotations  # postpone evaluation of annotations

from dataclasses import dataclass
from src.conditions.pieceCellOccupyBlocker.PieceCellOccupyBlockerFactory import PieceCellOccupyBlockerFactory

"""Model object for a board of chess game. A board has a size and a grid of cells."""


class Board:
    def __init__(self, board_size: int, cells: list[list[Cell]]):
        self.board_size: int = board_size
        self.cells: list[list[Cell]] = cells

    # Helper method to return cell to the left of current cell.
    def get_left_cell(self, cell: Cell) -> Cell:
        return self.get_cell_at_location(cell.x, cell.y - 1)

    # Helper method to return cell to the right of current cell.
    def get_right_cell(self, cell: Cell) -> Cell:
        return self.get_cell_at_location(cell.x, cell.y + 1)

    # Helper method to return cell to the up of current cell.
    def get_up_cell(self, cell: Cell) -> Cell:
        return self.get_cell_at_location(cell.x + 1, cell.y)

    #  Helper method to return cell to the down of current cell.
    def get_down_cell(self, cell: Cell) -> Cell:
        return self.get_cell_at_location(cell.x - 1, cell.y)

    # Helper method to return cell at a given location.
    def get_cell_at_location(self, x: int, y: int) -> Cell:
        if x >= self.board_size or x < 0:
            return None
        if y >= self.board_size or y < 0:
            return None

        return self.cells[x][y]

    # Helper method to determine whether the player is on check on the current board.
    def is_player_on_check(self, player: Player) -> bool:
        return self.check_if_piece_can_be_killed(player.get_pieces(PieceType.KING),
                                                 PieceCellOccupyBlockerFactory.king_check_evaluation_blockers(),
                                                 player)

    # Method to check if the piece can be killed currently by the opponent as per the current board configuration.
    '''
    @param targetPiece        Piece which is to be checked.
    @param cellOccupyBlockers Blockers which make cell un capable of occupying.
    @param player             Player whose piece has to be checked.
    @return Boolean indicating whether the piece is in danger or not.
    '''

    def check_if_piece_can_be_killed(self, target_piece: Piece, cell_occupy_blocker: list[iPieceCellOccupyBlocker],
                                     player: Player) -> bool:
        for x in range(self.board_size):
            for y in range(self.board_size):
                current_piece: Piece = self.get_cell_at_location(x, y).current_piece  # for every piece on the board

                if current_piece is not None and not (current_piece.is_piece_from_same_player(target_piece)):
                    next_possible_cells: list[Cell] = current_piece.next_possible_cells(self, cell_occupy_blocker,
                                                                                        player)
                    if target_piece.current_cell in next_possible_cells:
                        return True
        return False


class Cell:
    def __init__(self, x: int, y: int, current_piece: Piece = None):
        self.x: int = x
        self.y: int = y
        self.current_piece: Piece = current_piece

    def is_free(self) -> bool:
        return self.current_piece is None


from enum import Enum


class Color(Enum):
    BLACK = 1,
    WHITE = 2


from src.conditions.pieceCellOccupyBlocker.iPieceCellOccupyBlocker import iPieceCellOccupyBlocker
from src.excepetions.InvalidMoveException import InvalidMoveException
from src.moves.PossibleMovesProvider import PossibleMovesProvider


class Piece:

    def __init__(self, color: Color, moves_providers: list[PossibleMovesProvider],
                 piece_type: PieceType):
        self.is_killed: bool = False
        self.color: Color = color
        self.moves_providers: list[PossibleMovesProvider] = moves_providers
        self.num_moves: int = 0
        self.piece_type: PieceType = piece_type
        self.current_cell: Cell = None

    def kill_it(self):
        self.is_killed = True

    # Method to move piece from current cell to a given cell.
    def move(self, player: Player, to_cell: Cell, board: Board, additional_blockers: list[iPieceCellOccupyBlocker]):
        if self.is_killed:
            raise InvalidMoveException()
        next_possible_cells: list[Cell] = self.next_possible_cells(board, additional_blockers, player)

        if to_cell not in next_possible_cells:
            raise InvalidMoveException()
        self.kill_piece_in_cell(to_cell)
        self.current_cell.current_piece = None
        self.current_cell = to_cell
        self.current_cell.current_piece = self
        self.num_moves += 1

    # Helper method to kill a piece in a given cell
    def kill_piece_in_cell(self, target_cell: Cell):
        if target_cell.current_piece is not None:
            target_cell.current_piece.kill_it()

    def next_possible_cells(self, board: Board, additional_blockers: list[iPieceCellOccupyBlocker], player: Player) -> \
            list[Cell]:
        result: set[Cell] = set()
        for moves_provider in self.moves_providers:
            cells: list[Cell] = moves_provider.possible_moves(self, board, additional_blockers, player)
            if len(cells) != 0:
                for cell in cells:
                    result.add(cell)

        return list(result)

    def is_piece_from_same_player(self, piece: Piece) -> bool:
        return piece.color == self.color


from enum import Enum


class PieceType(Enum):
    KING = 1,
    QUEEN = 2,
    ROOK = 3,
    KNIGHT = 4,
    BISHOP = 5,
    PAWN = 6


from abc import ABC, abstractmethod

from src.excepetions.PieceNotFoundException import PieceNotFoundException

"""Abstract model class representing a player. This is abstract because we are not sure how player is going to make his
move. If the player is a local player, then he can move locally. A player can also be a network based player.
So, depending on the type of player, he can make move in its own way."""


class Player(ABC):
    def __init__(self, pieces: list[Piece]):
        self.pieces: list[Piece] = pieces

    def get_pieces(self, piece_type: PieceType) -> Piece:
        for piece in self.pieces:
            if piece.piece_type == piece_type:
                return piece
        raise PieceNotFoundException()

    @abstractmethod
    def make_move(self) -> PlayerMove:
        pass


@dataclass
class PlayerMove:
    piece: Piece
    to_cell: Cell
