from src.conditions.pieceCellOccupyBlocker.PieceCellOccupyBlockerKingCheck import PieceCellOccupyBlockerKingCheck
from src.conditions.pieceCellOccupyBlocker.PieceCellOccupyBlockerSelfPiece import PieceCellOccupyBlockerSelfPiece
from src.conditions.pieceCellOccupyBlocker.iPieceCellOccupyBlocker import iPieceCellOccupyBlocker


class PieceCellOccupyBlockerFactory:

    @classmethod
    def default_base_blocker(cls) -> iPieceCellOccupyBlocker:
        return PieceCellOccupyBlockerSelfPiece()

    @classmethod
    def default_additional_blockers(cls) -> list[iPieceCellOccupyBlocker]:
        return [PieceCellOccupyBlockerKingCheck()]

    @classmethod
    def king_check_evaluation_blockers(cls) -> list[iPieceCellOccupyBlocker]:
        return []
