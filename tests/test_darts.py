import pytest

from src.darts import XOhOne
from src.scoreboard import Stats, Turn
from src.game_options import GameOptions, ThrowReturn, CheckInOut
from src.general.throw import Throw


class TestingUI:
    def __init__(self, last_throw: str):
        self.last_throw = last_throw

    def display_game_start(self, game_opt: GameOptions) -> None:
        pass

    def display_scoreboard(
        self,
        stats: list[Stats],
        last_turns: list[Turn],
        game_options: GameOptions,
        clear_screen: bool = True,
    ) -> None:
        pass

    def display_game_options(self, game_opt: GameOptions) -> None:
        pass

    def read_throw(
        self, player: str, remaining_score: int, dart: int
    ) -> tuple[ThrowReturn, Throw]:
        return ThrowReturn.THROW, Throw(self.last_throw)

    def read_players(self) -> list[str]:
        return []

    def read_game_options(self, players: list[str]) -> GameOptions:
        return GameOptions()


straight_out = GameOptions()
straight_out.sets = 1
straight_out.legs = 1
straight_out.check_out = CheckInOut.STRAIGHT
double_out = GameOptions()
straight_out.sets = 1
double_out.legs = 1
double_out.check_out = CheckInOut.DOUBLE

twenty_four_score: list[tuple[GameOptions, str, str, bool]] = [
    (straight_out, "12", "12", True),
    (straight_out, "12", "d6", True),
    (straight_out, "12", "t4", True),
    (straight_out, "12", "11", False),
    (straight_out, "12", "13", False),
    (straight_out, "12", "d5", False),
    (straight_out, "12", "d7", False),
    (double_out, "12", "d6", True),
    (double_out, "12", "12", False),
    (double_out, "12", "d8", False),
    (double_out, "12", "13", False),
    (double_out, "12", "11", False),
    (double_out, "12", "d5", False),
    (double_out, "11", "12", False),
    (double_out, "11", "d6", False),
    (double_out, "11", "13", False),
]


@pytest.mark.parametrize("game_opt,second_to_last_throw,last_throw,result", twenty_four_score)
def test_darts(
    game_opt: GameOptions, second_to_last_throw: str, last_throw: str, result: bool
) -> None:
    players = ["test_player"]
    to_twenty_four = ["t20", "t20", "t20", "t20", "t20", "t20", "t20", "t19"]
    to_twenty_four.append(second_to_last_throw)
    game = XOhOne(TestingUI(last_throw), players, game_opt)
    for player in players:
        game.scoreboard.register_player(player)
        for dart in to_twenty_four:
            game.scoreboard.add_throw(player, Throw(dart), 0)
    assert game.do_player_round() == result
