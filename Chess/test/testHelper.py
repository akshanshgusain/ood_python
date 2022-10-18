from src.conditions.PieceMoveFurtherCondition.PieceMoveFurtherConditionDefault import PieceMoveFurtherConditionDefault
from src.conditions.moveBaseCondition.NoMoveBaseCondition import NoMoveBaseCondition
from src.conditions.pieceCellOccupyBlocker.PieceCellOccupyBlockerFactory import PieceCellOccupyBlockerFactory
from src.conditions.pieceCellOccupyBlocker.iPieceCellOccupyBlocker import iPieceCellOccupyBlocker
from src.models.board import Board
from src.models.cell import Cell
from src.models.color import Color
from src.models.piece import Piece
from src.models.pieceType import PieceType
from src.moves.PossibleMovesProvider import PossibleMovesProvider
from src.moves.PossibleMovesProviderDiagonal import PossibleMovesProviderDiagonal
from src.moves.PossibleMovesProviderHorizontal import PossibleMovesProviderHorizontal
from src.moves.PossibleMovesProviderVertical import PossibleMovesProviderVertical
from src.moves.VerticalMoveDirection import VerticalMoveDirection


class TestHelpers:

    @classmethod
    def create_board(cls) -> Board:
        cells: list[list[Cell]] = []
        for i in range(8):
            for j in range(8):
                cells[i][j] = Cell(i, j)

        return Board(8, cells)

    @classmethod
    def piece_set(cls, color: Color, board: Board, main_pieces_row_num: int, pawn_piece_row_num: int,
                  pawn_direction: VerticalMoveDirection) -> list[Piece]:
        all_pieces: list[Piece] = []

        # Create Pawn Pieces
        for i in range(8):
            pawn: Piece = cls.pawn(color, pawn_direction)
            cls.add_piece_to_board(board, pawn, pawn_piece_row_num, i)
            all_pieces.append(pawn)

        # Create Main Pieces

        king: Piece = cls.king(color)
        cls.add_piece_to_board(board, king, main_pieces_row_num, 3)

        queen: Piece = cls.queen(color)
        cls.add_piece_to_board(board, queen, main_pieces_row_num, 4)

        queen: Piece = cls.queen(color)
        cls.add_piece_to_board(board, queen, main_pieces_row_num, 4)

        rook1: Piece = cls.rook(color)
        cls.add_piece_to_board(board, rook1, main_pieces_row_num, 0)
        rook2: Piece = cls.rook(color)
        cls.add_piece_to_board(board, rook2, main_pieces_row_num, 7)

        bishop1: Piece = cls.bishop(color)
        cls.add_piece_to_board(board, bishop1, main_pieces_row_num, 2)
        bishop2: Piece = cls.bishop(color)
        cls.add_piece_to_board(board, bishop2, main_pieces_row_num, 5)

        knight1: Piece = cls.knight(color)
        cls.add_piece_to_board(board, knight1, main_pieces_row_num, 1)
        knight2: Piece = cls.knight(color)
        cls.add_piece_to_board(board, knight2, main_pieces_row_num, 6)

        main_pieces: list[Piece] = [king, queen, knight1, knight2, bishop1, bishop2, rook1, rook2]
        all_pieces.extend(main_pieces)
        return all_pieces

    @classmethod
    def add_piece_to_board(cls, board: Board, piece: Piece, row: int, col: int):
        cell: Cell = board.get_cell_at_location(row, col)
        piece.current_cell = cell
        cell.current_piece = piece

    @classmethod
    def random_pieces(cls):
        return cls.pawn(Color.WHITE, VerticalMoveDirection.BOTH)

    @classmethod
    def test_pieces(cls, color: Color, piece_type: PieceType):
        return Piece(color, [], piece_type)

    # Pieces
    @classmethod
    def pawn(cls, color: Color, pawn_direction: VerticalMoveDirection) -> Piece:
        pawn_move_providers: list[PossibleMovesProvider] = [
            PossibleMovesProviderVertical(1, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker(), pawn_direction),
            PossibleMovesProviderVertical(2, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker(), pawn_direction)
        ]
        return Piece(color, pawn_move_providers, PieceType.PAWN)

    @classmethod
    def king(cls, color: Color) -> Piece:
        king_move_provider: list[PossibleMovesProvider] = [
            PossibleMovesProviderVertical(1, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker(), VerticalMoveDirection.BOTH),
            PossibleMovesProviderHorizontal(1, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                            cls.default_base_blocker()),
            PossibleMovesProviderDiagonal(1, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker())
        ]
        return Piece(color, king_move_provider, PieceType.KING)

    @classmethod
    def queen(cls, color: Color) -> Piece:
        queen_move_provider: list[PossibleMovesProvider] = [
            PossibleMovesProviderVertical(8, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker(), VerticalMoveDirection.BOTH),
            PossibleMovesProviderHorizontal(8, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                            cls.default_base_blocker()),
            PossibleMovesProviderDiagonal(8, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker())
        ]
        return Piece(color, queen_move_provider, PieceType.QUEEN)

    @classmethod
    def rook(cls, color: Color) -> Piece:
        rook_move_provider: list[PossibleMovesProvider] = [
            PossibleMovesProviderVertical(8, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker(), VerticalMoveDirection.BOTH),
            PossibleMovesProviderHorizontal(8, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                            cls.default_base_blocker()),

        ]
        return Piece(color, rook_move_provider, PieceType.ROOK)

    @classmethod
    def bishop(cls, color: Color) -> Piece:
        bishop_move_provider: list[PossibleMovesProvider] = [

            PossibleMovesProviderDiagonal(8, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker())
        ]
        return Piece(color, bishop_move_provider, PieceType.BISHOP)

    @classmethod
    def knight(cls, color: Color) -> Piece:
        knight_move_provider: list[PossibleMovesProvider] = [

            PossibleMovesProviderDiagonal(1, NoMoveBaseCondition(), cls.default_move_further_condition(),
                                          cls.default_base_blocker())
        ]
        return Piece(color, knight_move_provider, PieceType.KNIGHT)

    @classmethod
    def default_move_further_condition(cls) -> PieceMoveFurtherConditionDefault:
        return PieceMoveFurtherConditionDefault()

    @classmethod
    def default_base_blocker(cls) -> iPieceCellOccupyBlocker:
        return PieceCellOccupyBlockerFactory().default_base_blocker()
