import pytest

from src.scoreboard import Scoreboard, is_overthrow
from src.game_options import GameOptions, CheckInOut, InputMethod
from src.throw import Throw


current_player_data: list[tuple[int, int, int]] = [
    (0, 0, 0),
    (0, 1, 0),
    (0, 2, 0),
    (0, 3, 1),
    (0, 4, 1),
    (0, 5, 1),
    (0, 6, 2),
    (0, 7, 2),
    (0, 8, 2),
    (0, 9, 0),

    (1, 0, 1),
    (1, 1, 1),
    (1, 2, 1),
    (1, 3, 2),
    (1, 4, 2),
    (1, 5, 2),
    (1, 6, 0),
    (1, 7, 0),
    (1, 8, 0),
    (1, 9, 1),
]


@pytest.mark.parametrize("start_player, darts,current_player", current_player_data)
def test_get_current_player(
    start_player: int,
    darts: int,
    current_player: int,
) -> None:
    game_options = GameOptions(start_player=start_player, sets=1, legs=1)
    game_options.input_method = InputMethod.THREEDARTS
    scoreboard = Scoreboard(game_options)
    for player in ["a", "b", "c"]:
        scoreboard.register_player(player)
    for i in range(darts):
        manuel_player = scoreboard.get_players()[((i // 3) + start_player) % 3]
        scoreboard.add_throw(manuel_player, Throw("1"), i % 3)
    print(scoreboard.get_history())
    assert scoreboard.get_current_player() == scoreboard.get_players()[current_player]


starting_data: list[tuple[int, int, int, int]] = [
    (0, 0, 0, 0),
    (0, 0, 1, 1),
    (0, 0, 2, 2),
    (0, 1, 0, 1),
    (0, 1, 1, 2),
    (0, 1, 2, 0),
    (1, 0, 0, 1),
    (1, 0, 1, 2),
    (1, 0, 2, 0),
    (1, 1, 0, 2),
    (1, 1, 1, 0),
    (1, 1, 2, 1),
    (2, 0, 0, 2),
    (2, 0, 1, 0),
    (2, 0, 2, 1),
    (2, 1, 0, 0),
    (2, 1, 1, 1),
    (2, 1, 2, 2),
]


@pytest.mark.parametrize(
    "set_start_player,won_sets,won_legs,start_player", starting_data
)
def test_get_start_player_of_leg(
    set_start_player: int,
    won_sets: int,
    won_legs: int,
    start_player: int,
) -> None:
    to_win = ["t20", "t20", "t20", "t20", "t20", "t20", "t20", "t19", "d12"]
    game_options = GameOptions()
    game_options.start_player = set_start_player
    game_options.sets = 2
    game_options.legs = 3
    game_options.input_method = InputMethod.THREEDARTS
    scoreboard = Scoreboard(game_options)
    for player in ["a", "b", "c"]:
        any_player = scoreboard.register_player(player)
    for won_set in range(won_sets):
        for won_leg in range(game_options.legs):
            for dart, throw in enumerate(to_win):
                scoreboard.add_throw(any_player, Throw(throw), dart % 3)
            scoreboard.append_hist_if_winning_throw(any_player)
    for won_leg in range(won_legs):
        for dart, throw in enumerate(to_win):
            scoreboard.add_throw(any_player, Throw(throw), dart % 3)
        scoreboard.append_hist_if_winning_throw(any_player)
    assert scoreboard.get_start_player_of_leg() == scoreboard.get_players()[start_player]


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
    player = scoreboard.register_player("player")
    for dart in to_twenty_four:
        scoreboard.add_throw(player, Throw(dart), 0)
    assert scoreboard.get_remaining_score_of(player) == remaining_score


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
    player = scoreboard.register_player("player")
    for dart in to_twenty_four:
        scoreboard.add_throw(player, Throw(dart), 0)
    remaining_score = scoreboard.get_remaining_score_of(player)
    assert (
        is_overthrow(remaining_score, Throw(last_throw), game_options.check_out)
        == result
    )
