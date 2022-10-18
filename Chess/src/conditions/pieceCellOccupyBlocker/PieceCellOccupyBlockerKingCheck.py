from src.conditions.pieceCellOccupyBlocker.iPieceCellOccupyBlocker import iPieceCellOccupyBlocker
from src.models.board import Board
from src.models.cell import Cell
from src.models.piece import Piece
from src.models.player import Player

''' This tells whether making piece move to a cell will attract check for king. '''


class PieceCellOccupyBlockerKingCheck(iPieceCellOccupyBlocker):

    def is_cell_non_occupiable_for_piece(self, cell: Cell, piece: Piece, board: Board, player: Player) -> bool:
        piece_original_cell: Cell = piece.current_cell
        piece.current_cell = cell
        player_getting_check_by_move: bool = board.is_player_on_check(player)
        piece.current_cell = piece_original_cell
        return player_getting_check_by_move
