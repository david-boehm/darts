import pytest

from src.scoreboard import Scoreboard, set_start_player, is_overthrow
from src.game_options import GameOptions, CheckInOut
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


straight_out = GameOptions()
straight_out.sets = 1
straight_out.legs = 1
straight_out.check_out = CheckInOut.STRAIGHT
double_out = GameOptions()
straight_out.sets = 1
double_out.legs = 1
double_out.check_out = CheckInOut.DOUBLE

twenty_four_score: list[tuple[GameOptions, str, str, int, bool]] = [
    (straight_out, "12", "12", 0, False),
    (straight_out, "12", "d6", 0, False),
    (straight_out, "12", "t4", 0, False),
    (straight_out, "12", "11", 1, False),
    (straight_out, "12", "d5", 2, False),
    (straight_out, "12", "13", 12, True),
    (straight_out, "12", "d7", 12, True),
    (double_out, "12", "d6", 0, False),
    (double_out, "12", "12", 12, True),
    (double_out, "12", "d7", 12, True),
    (double_out, "12", "13", 12, True),
    (double_out, "12", "11", 12, True),
    (double_out, "12", "d5", 2, False),
    (double_out, "11", "12", 13, True),
    (double_out, "11", "d6", 13, True),
    (double_out, "11", "13", 13, True),
]


@pytest.mark.parametrize(
    "game_options,second_to_last_throw,last_throw,remaining_score,_",
    twenty_four_score,
)
def test_subtract(
    game_options: GameOptions,
    second_to_last_throw: str,
    last_throw: str,
    remaining_score: int,
    _: bool,
) -> None:
    to_twenty_four = ["t20", "t20", "t20", "t20", "t20", "t20", "t20", "t19"]
    to_twenty_four.extend([second_to_last_throw, last_throw])
    scoreboard = Scoreboard(game_options)
    scoreboard.register_player("player")
    for dart in to_twenty_four:
        scoreboard.add_throw("player", Throw(dart), 0)
    assert scoreboard.get_remaining_score_of("player") == remaining_score


@pytest.mark.parametrize(
    "game_options,second_to_last_throw,last_throw,_,result",
    twenty_four_score,
)
def test_is_overthrow(
    game_options: GameOptions,
    second_to_last_throw: str,
    last_throw: str,
    _: int,
    result: bool,
) -> None:
    to_twenty_four = ["t20", "t20", "t20", "t20", "t20", "t20", "t20", "t19"]
    to_twenty_four.extend([second_to_last_throw])
    scoreboard = Scoreboard(game_options)
    scoreboard.register_player("player")
    for dart in to_twenty_four:
        scoreboard.add_throw("player", Throw(dart), 0)
    remaining_score = scoreboard.get_remaining_score_of("player")
    assert (
        is_overthrow(remaining_score, Throw(last_throw), game_options.check_out)
        == result
    )
