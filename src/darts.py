import sys

from src.ui import UI
from src.game_options import GameOptions, ThrowReturn
from src.scoreboard import Scoreboard, set_start_player


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
        player = 0
        throw_in_round = 0
        players = set_start_player(
            self.players,
            self.game_options.start_player,
            *self.scoreboard.get_won_sets_and_legs(),
        )
        while player < len(players):
            undo_player = False
            while throw_in_round < self.game_options.input_method.value:
                self.ui.display_scoreboard(
                    self.scoreboard.get_all_stats(),
                    self.scoreboard.get_turns_of_leg()[0 : 3 * player + throw_in_round],
                    self.game_options,
                )
                throw_return, throw = self.ui.read_throw(
                    players[player],
                    self.scoreboard.get_remaining_score_of(players[player]),
                    throw_in_round,
                )
                if throw_return == ThrowReturn.EXIT:
                    sys.exit("The game was canceled")
                elif throw_return == ThrowReturn.UNDO:
                    if self.scoreboard.undo_throw():
                        if throw_in_round == 0:
                            undo_player = True
                            break
                        throw_in_round -= 1
                    continue
                self.scoreboard.add_throw(
                    players[player], throw, throw_in_round
                )
                throw_in_round += 1
                if self.scoreboard.was_overthrow(players[player]):
                    break
                if self.scoreboard.append_hist_if_winning_throw(players[player]):
                    return self.scoreboard.is_win("game", players[player])

            if undo_player:
                throw_in_round = self.game_options.input_method.value - 1
                if player > 0:
                    player -= 1
                else:
                    player = len(players) - 1
            else:
                player += 1
                throw_in_round = 0
        return False
