from typing import Protocol


from src.scoreboard import Stats, Turn
from src.game_options import GameOptions, ThrowReturn
from src.general.throw import Throw


class UI(Protocol):
    def display_game_start(self, game_opt: GameOptions) -> None:
        ...

    def display_scoreboard(
        self,
        stats: list[Stats],
        last_turns: list[Turn],
        game_options: GameOptions,
        clear_screen: bool = True,
    ) -> None:
        ...

    def display_game_options(self, game_opt: GameOptions) -> None:
        ...

    def read_throw(
        self, player: str, remaining_score: int, dart: int
    ) -> tuple[ThrowReturn, Throw]:
        ...

    def read_players(self) -> list[str]:
        ...

    def read_game_options(self, players: list[str]) -> GameOptions:
        ...
