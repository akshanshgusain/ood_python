from src.conditions.pieceCellOccupyBlocker.PieceCellOccupyBlockerFactory import PieceCellOccupyBlockerFactory
from gameplay.contracts.player_move import PlayerMove
from src.models.board import Board
from src.models.player import Player


class GameController:

    @classmethod
    def gameplay(cls, players: list[Player], board: Board):
        current_player: int = 0
        while True:
            player: Player = players[current_player]
            player_move: PlayerMove = player.make_move()
            player_move.piece.move(player, player_move.to_cell, board,
                                   PieceCellOccupyBlockerFactory.default_additional_blockers())
            current_player = (current_player + 1) % len(players)
