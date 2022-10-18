import unittest

from src.models.models import *
from src.moves.VerticalMoveDirection import VerticalMoveDirection
from testHelper import TestHelpers


class TestPlayer(Player):
    def __init__(self, pieces: list[Piece]):
        super(TestPlayer, self).__init__(pieces)

    def make_move(self) -> PlayerMove:
        return None


class BaseTest(unittest.TestCase):

    def test_sample_gameplay(self):
        board: Board = TestHelpers.create_board()
        white_pieces: list[Piece] = TestHelpers.piece_set(Color.WHITE, board, 0, 1, VerticalMoveDirection.UP)
        black_pieces: list[Piece] = TestHelpers.piece_set(Color.BLACK, board, 7, 6, VerticalMoveDirection.DOWN)

        white_player: Player = TestPlayer(white_pieces)
        black_player: Player = TestPlayer(black_pieces)

        self.print_board(board, "Initial")

        # Validate that queen has no possible moves initially
        white_queen: Piece = board.get_cell_at_location(0, 4).current_piece
        self.assertEqual(white_queen.color, Color.WHITE)
        self.assertEqual(white_queen.piece_type, PieceType.QUEEN)

    @classmethod
    def print_board(cls, board: Board, title: str):
        print(f"\n\n {title}")
        for i in range(board.board_size, -1, -1):
            for j in range(board.board_size):
                print(cls.display_char(board.get_cell_at_location(i, j)))

    @classmethod
    def display_char(cls, cell: Cell) -> str:
        return " "