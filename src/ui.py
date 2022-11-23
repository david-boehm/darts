from typing import Protocol


from src.scoreboard import Stats
from src.game_options import GameOptions, ThrowReturn
from src.general.throw import Throw


class UI(Protocol):
    def write(self, message: str) -> None:
        raise NotImplementedError

    def display_scoreboard(self, stats: list[Stats], clear_screen: bool = True) -> None:
        raise NotImplementedError

    def display_game_options(self, game_opt: GameOptions) -> None:
        raise NotImplementedError

    def overthrow(self) -> None:
        raise NotImplementedError

    def read_players(self) -> list[str]:
        raise NotImplementedError

    def read_game_options(self, players: list[str]) -> GameOptions:
        raise NotImplementedError

    def read_throw(self, message: str) -> tuple[ThrowReturn, Throw]:
        raise NotImplementedError
