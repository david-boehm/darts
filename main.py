#!/usr/bin/python
import sys

from src.game_options import GameOptions, GameMode, ThrowReturn
from src.scoreboard import Scoreboard
from src.general.throw import Throw
from src.cli import CLI

def set_start_player(players: list[str], start_player: int, sets: dict[str,int], legs: dict[str,int]) -> list[str]:
    # sets, legs = self.scoreboard.get_won_sets_and_legs()
    shift_legs = sum(legs.values()) % len(players)
    shift_sets = sum(sets.values()) % len(players)
    # if shift_sets + shift_legs + start_player == len(players):
    #   return players
    rotated_players = players.copy()
    for i in range((shift_sets + shift_legs + start_player) % len(players)):
        rotated_players.append(rotated_players.pop(0))
    return rotated_players

class Darts():
    def __init__(self, ui:CLI , players: list[str], game_opt: GameOptions) -> None:
        self.ui = ui
        self.scoreboard = Scoreboard(game_opt)
        self.players = players
        self.game_opt = game_opt
        # self.ui.write(f"players found: {self.players}")
        # self.ui.write(f"Game options {self.game_opt}")

    def play(self) -> None:
        self.ui.display_game_options(self.game_opt)
        self.ui.write("--- Game on! ---")
        if self.game_opt.game_mode == GameMode.X01:
            game_won = False
            for player in self.players:
                self.scoreboard.register_player(player)
            self.ui.display_scoreboard(self.scoreboard.get_all_stats(),False)
            while not game_won:
                game_won = self.do_X01_round()
                self.ui.display_scoreboard(self.scoreboard.get_all_stats())

    def do_X01_round(self) -> bool:
        player_int = 0
        dart = 0
        player_list = set_start_player(self.players, self.game_opt.start_player, *self.scoreboard.get_won_sets_and_legs())
        while player_int < len(player_list):
            undo_player = False
            player = player_list[player_int]
            self.ui.write(f"\nDarts of {player} - (prefix d for double or t for tripple + Number, eg t20): ")
            while dart < self.game_opt.input_method.value:
                throw_return, throw = self.ui.read_throw(f"{player} requires: {self.scoreboard.get_remaining_score_of_player(player)} - Dart {dart+1}: ")
                if throw_return == ThrowReturn.EXIT:
                    sys.exit(f"The game was canceled")
                elif throw_return == ThrowReturn.UNDO:
                    if self.scoreboard.undo_throw():
                        if dart == 0:
                            undo_player = True
                            break
                        dart -= 1
                    continue
                remaining_score = self.scoreboard.get_remaining_score_of_player(player)
                self.scoreboard.add_throw(player, throw)
                dart += 1
                if remaining_score == throw.calc_score() :
                    return self.scoreboard.is_win("game", player, throw)
                elif remaining_score < throw.calc_score():
                    self.ui.overthrow()
                
            if undo_player:
                dart = self.game_opt.input_method.value - 1
                if player_int > 0:
                    player_int -= 1
                else:
                    player_int = len(player_list) - 1
            else:
                player_int += 1
                dart = 0
        return False


def main() -> None:
    ui = CLI()
    players = ui.read_players()
    game_opt = ui.read_game_options(players)
    game = Darts(ui, players, game_opt)
    game.play()

if __name__ == "__main__":
    main()
