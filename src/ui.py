from typing import Protocol


from src.scoreboard import Stats
from src.game_options import GameOptions, ThrowReturn, InputMethod
from src.general.throw import Throw


class UI(Protocol):
    def write(self, message: str) -> None:
        ...

    def display_game_start(self, game_opt: GameOptions) -> None:
        ...

    def display_scoreboard(self, stats: list[Stats], clear_screen: bool = True) -> None:
        ...

    def display_game_options(self, game_opt: GameOptions) -> None:
        ...

    def overthrow(self) -> None:
        ...

    def read_players(self) -> list[str]:
        ...

    def read_game_options(self, players: list[str]) -> GameOptions:
        ...

    def read_throw(
        self, player: str, remaining_score: int, dart: int
    ) -> tuple[ThrowReturn, Throw]:
        ...

    def display_new_round(self, player: str, input_method: InputMethod) -> None:
        ...
