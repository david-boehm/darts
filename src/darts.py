import sys

from src.ui import UI
from src.game_options import GameOptions, GameMode, ThrowReturn
from src.scoreboard import Scoreboard
from src.general.throw import Throw


def set_start_player(
    players: list[str], start_player: int, sets: dict[str, int], legs: dict[str, int]
) -> list[str]:
    # sets, legs = self.scoreboard.get_won_sets_and_legs()
    shift_legs = sum(legs.values()) % len(players)
    shift_sets = sum(sets.values()) % len(players)
    # if shift_sets + shift_legs + start_player == len(players):
    #   return players
    rotated_players = players.copy()
    for i in range((shift_sets + shift_legs + start_player) % len(players)):
        rotated_players.append(rotated_players.pop(0))
    return rotated_players


class XOhOne:
    def __init__(self, ui: UI, players: list[str], game_opt: GameOptions) -> None:
        self.ui = ui
        self.scoreboard = Scoreboard(game_opt)
        self.players = players
        self.game_opt = game_opt
        # self.ui.write(f"players found: {self.players}")
        # self.ui.write(f"Game options {self.game_opt}")

    def play(self) -> None:
        self.ui.display_game_start(self.game_opt)
        if self.game_opt.game_mode == GameMode.X01:
            game_won = False
            for player_name in self.players:
                self.scoreboard.register_player(player_name)
            self.ui.display_scoreboard(self.scoreboard.get_all_stats(), False)
            while not game_won:
                game_won = self.do_player_round()
                self.ui.display_scoreboard(self.scoreboard.get_all_stats())

    def do_player_round(self) -> bool:
        player = 0
        dart = 0
        players = set_start_player(
            self.players,
            self.game_opt.start_player,
            *self.scoreboard.get_won_sets_and_legs(),
        )
        while player < len(players):
            undo_player = False
            self.ui.display_new_round(players[player], self.game_opt.input_method)
            while dart < self.game_opt.input_method.value:
                throw_return, throw = self.ui.read_throw(
                    players[player],
                    self.scoreboard.get_remaining_score_of(players[player]),
                    dart,
                )
                if throw_return == ThrowReturn.EXIT:
                    sys.exit("The game was canceled")
                elif throw_return == ThrowReturn.UNDO:
                    if self.scoreboard.undo_throw():
                        if dart == 0:
                            undo_player = True
                            break
                        dart -= 1
                    continue
                is_leg_win = self.scoreboard.add_throw(players[player], throw)
                dart += 1
                if is_leg_win:
                    return self.scoreboard.is_win("game", players[player])
                elif self.scoreboard.is_overthrow(players[player]):
                    self.ui.overthrow()

            if undo_player:
                dart = self.game_opt.input_method.value - 1
                if player > 0:
                    player -= 1
                else:
                    player = len(players) - 1
            else:
                player += 1
                dart = 0
        return False
