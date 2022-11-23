import pytest

from src.darts import Darts, set_start_player
from src.scoreboard import Stats
from src.game_options import GameOptions, ThrowReturn
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
    def __init__(self, last_dart: str):
        self.last_dart = last_dart

    def write(self, message: str) -> None:
        pass

    def display_scoreboard(self, stats: list[Stats], clear_screen: bool = True) -> None:
        pass

    def display_game_options(self, game_opt: GameOptions) -> None:
        pass

    def overthrow(self) -> None:
        pass

    def read_players(self) -> list[str]:
        return []

    def read_game_options(self, players: list[str]) -> GameOptions:
        return GameOptions()

    def read_throw(self, message: str) -> tuple[ThrowReturn, Throw]:
        throw = Throw(self.last_dart)
        throw.is_valid_input()
        return ThrowReturn.THROW, throw


players = ["test1"]
double_out = GameOptions()
double_out.legs = 1
played_darts = ["t20", "t20", "t20", "t20", "t20", "t20", "t20", "t19", "12"]

test_game_data: list[tuple[list[str], GameOptions, list[str], str, bool]] = [
    (players, double_out, played_darts, "d6", True),
    (players, double_out, played_darts, "12", False),
]


@pytest.mark.parametrize("players,game_opt,played_darts,last_dart,result", test_game_data)
def test_darts(
    players: list[str],
    game_opt: GameOptions,
    played_darts: list[str],
    last_dart: str,
    result: bool
) -> None:
    game = Darts(TestingUI(last_dart), players, game_opt)
    for player in players:
        game.scoreboard.register_player(player)
    for dart in played_darts:
        game.scoreboard.add_throw(players[0], Throw(dart))
    assert game.do_X01_round() == result
