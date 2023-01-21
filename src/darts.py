import sys

from src.ui import UI
from src.game_options import GameOptions, ThrowReturn
from src.scoreboard import Scoreboard


class XOhOne:
    def __init__(self, ui: UI, players: list[str], game_options: GameOptions) -> None:
        self.ui = ui
        self.scoreboard = Scoreboard(game_options)
        self.players = players
        self.game_options = game_options

    def play(self) -> None:
        for player_name in self.players:
            self.scoreboard.register_player(player_name)
        self.ui.display_game_start(self.game_options)
        while not self.do_player_round():  # game not won
            ...  # Do some stuff if more than two are playing

    def do_player_round(self) -> bool:
        player, throw_in_round = self.scoreboard.current_player()
        self.ui.display_scoreboard(
            self.scoreboard.get_all_stats(),
            self.scoreboard.turns_of_current_round(),
            self.game_options,
        )
        throw_return, throw = self.ui.read_throw(
            player.name,
            self.scoreboard.get_remaining_score_of(player),
            throw_in_round,
        )
        if throw_return == ThrowReturn.EXIT:
            sys.exit("The game was canceled")
        elif throw_return == ThrowReturn.UNDO:
            if self.scoreboard.undo_throw():
                return False
        self.scoreboard.add_throw(player, throw, throw_in_round)
        if self.scoreboard.was_overthrow(player):
            return False
        if self.scoreboard.append_hist_if_winning_throw(player):
            return self.scoreboard.is_win("game", player)
        return False
