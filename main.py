#!/usr/bin/python
import sys

from src.cli import CLI
from src.darts import XOhOne
from src.game_options import GameMode


def main() -> None:
    ui = CLI()
    players = ui.read_players()
    if not len(players):
        sys.exit("The game was canceled, no players found")
    game_opt = ui.read_game_options(players)
    if game_opt.game_mode == GameMode.XOhOne:
        game = XOhOne(ui, players, game_opt)
    game.play()


if __name__ == "__main__":
    main()
