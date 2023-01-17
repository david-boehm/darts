import pytest

from src.darts import XOhOne, set_start_player
from src.scoreboard import Stats, Turn
from src.game_options import GameOptions, ThrowReturn, CheckInOut, InputMethod
from src.general.throw import Throw


def rotate(players: list[str], rotations: int) -> list[str]:
    _players = players.copy()
    for i in range(rotations):
        _players.append(_players.pop(0))
    return _players


def add_win(
    dict_to_add: dict[str, int], key_to_add: str, value_to_set: int
) -> dict[str, int]:
    _dict_to_add = dict_to_add.copy()
    _dict_to_add[key_to_add] = value_to_set
    return _dict_to_add


players = ["a", "b", "c"]
sets = {"a": 0, "b": 0, "c": 0}
legs = {"a": 0, "b": 0, "c": 0}


test_data = [
    (players, 0, sets, legs, rotate(players, 0)),
    (players, 1, sets, legs, rotate(players, 1)),
    (players, 2, sets, legs, rotate(players, 2)),
    (players, 0, sets, add_win(legs, "a", 1), rotate(players, 1)),
    (players, 0, sets, add_win(legs, "b", 2), rotate(players, 2)),
    (players, 0, sets, add_win(legs, "c", 3), rotate(players, 3)),
    (players, 1, sets, add_win(legs, "a", 1), rotate(players, 2)),
    (players, 1, sets, add_win(legs, "b", 2), rotate(players, 3)),
    (players, 1, sets, add_win(legs, "c", 3), rotate(players, 4)),
    (players, 0, add_win(sets, "a", 1), legs, rotate(players, 1)),
    (players, 0, add_win(sets, "a", 1), add_win(legs, "a", 1), rotate(players, 2)),
    (players, 0, add_win(sets, "a", 1), add_win(legs, "b", 2), rotate(players, 3)),
    (players, 0, add_win(sets, "a", 1), add_win(legs, "c", 3), rotate(players, 4)),
    (players, 1, add_win(sets, "a", 1), legs, rotate(players, 2)),
    (players, 1, add_win(sets, "a", 1), add_win(legs, "a", 1), rotate(players, 3)),
    (players, 1, add_win(sets, "a", 1), add_win(legs, "b", 2), rotate(players, 4)),
    (players, 1, add_win(sets, "a", 1), add_win(legs, "c", 3), rotate(players, 5)),
]


@pytest.mark.parametrize("players,start_player,sets,legs,rotated_players", test_data)
def test_set_start_player(
    players: list[str],
    start_player: int,
    sets: dict[str, int],
    legs: dict[str, int],
    rotated_players: list[str],
) -> None:
    assert set_start_player(players, start_player, sets, legs) == rotated_players


class TestingUI:
    def __init__(self, last_throw: str):
        self.last_throw = last_throw

    def display_game_start(self, game_opt: GameOptions) -> None:
        pass

    def display_scoreboard(
        self,
        stats: list[Stats],
        last_turns: list[Turn],
        input_method: InputMethod,
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

test_game_data: list[tuple[GameOptions, str, str, bool]] = [
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


@pytest.mark.parametrize("game_opt,second_to_last_throw,last_throw,result", test_game_data)
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
