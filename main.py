#!/usr/bin/python
import sys

from src.cli import CLI
from src.darts import Darts


def main() -> None:
    ui = CLI()
    players = ui.read_players()
    if not len(players):
        sys.exit("The game was canceled, no players found")
    game_opt = ui.read_game_options(players)
    game = Darts(ui, players, game_opt)
    game.play()


if __name__ == "__main__":
    main()
