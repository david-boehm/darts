import pytest

from src.scoreboard import Scoreboard, is_overthrow, Player, Turn
from src.game_options import GameOptions, CheckInOut, InputMethod
from src.throw import Throw


def test_register_player():
    game_options = GameOptions()
    scoreboard = Scoreboard(game_options)
    scoreboard.register_player("tester")
    assert scoreboard.players == [Player(idf=0, name="tester")]


def test_add_throw():
    game_options = GameOptions(start_points=501, input_method=InputMethod.THREEDARTS)
    scoreboard = Scoreboard(game_options)
    player = scoreboard.register_player("tester")
    scoreboard.add_throw(player, Throw("t20"), 0)
    assert (
        scoreboard.history[-1][-1][-1]
        == Turn(player=player, score=501, throw=Throw("t20"), throw_in_round=0)
        and len(scoreboard.history[-1][-1]) == 1
    )


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
    "set_start_player, won_sets, won_legs, start_player", starting_data
)
def test_get_start_player_of_leg(
    set_start_player: int,
    won_sets: int,
    won_legs: int,
    start_player: int,
) -> None:
    game_options = GameOptions(
        start_player=set_start_player,
        sets=2,
        legs=3,
        start_points=10,
        input_method=InputMethod.THREEDARTS,
    )
    scoreboard = Scoreboard(game_options)
    for player in ["a", "b", "c"]:
        scoreboard.register_player(player)
    for won_set in range(won_sets):
        for won_leg in range(game_options.legs):
            # two players must finish to end a leg
            for i in range(2):
                scoreboard.add_throw(scoreboard.get_players()[i], Throw("d5"), 0)
            scoreboard.append_hist_if_leg_finished()
    for won_leg in range(won_legs):
        for i in range(2):
            scoreboard.add_throw(scoreboard.get_players()[i], Throw("d5"), 0)
        scoreboard.append_hist_if_leg_finished()
    assert scoreboard.start_player_of_leg() == scoreboard.get_players()[start_player]


current_player_data: list[tuple[int, int, int, int]] = [
    (0, 0, 0, 0),
    (0, 1, 0, 1),
    (0, 2, 0, 2),
    (0, 3, 1, 0),
    (0, 4, 1, 1),
    (0, 5, 1, 2),
    (0, 6, 2, 0),
    (0, 7, 2, 1),
    (0, 8, 2, 2),
    (0, 9, 0, 0),
    (1, 0, 1, 0),
    (1, 1, 1, 1),
    (1, 2, 1, 2),
    (1, 3, 2, 0),
    (1, 4, 2, 1),
    (1, 5, 2, 2),
    (1, 6, 0, 0),
    (1, 7, 0, 1),
    (1, 8, 0, 2),
    (1, 9, 1, 0),
]


@pytest.mark.parametrize(
    "start_player, darts, current_player, current_dart", current_player_data
)
def test_current_player_and_throw(
    start_player: int,
    darts: int,
    current_player: int,
    current_dart: int,
) -> None:
    game_options = GameOptions(
        start_player=start_player, sets=1, legs=1, input_method=InputMethod.THREEDARTS
    )
    scoreboard = Scoreboard(game_options)
    for player in ["a", "b", "c"]:
        scoreboard.register_player(player)
    for i in range(darts):
        manuel_player = scoreboard.get_players()[((i // 3) + start_player) % 3]
        scoreboard.add_throw(manuel_player, Throw("1"), i % 3)
    print(scoreboard.get_history())
    assert scoreboard.current_player_and_throw() == (
        scoreboard.get_players()[current_player],
        current_dart,
    )


current_player_if_data: list[tuple[int, list[tuple[int, str, int]], int]] = [
    (  # zero test
        0,
        [],
        0,
    ),
    (  # normal score test
        0,
        [
            (0, "5", 0),
        ],
        0,
    ),
    (  # normal score test
        0,
        [
            (0, "1", 0),
            (0, "1", 1),
            (0, "1", 2),
        ],
        1,
    ),
    (  # win test
        0,
        [
            (0, "d5", 0),
        ],
        1,
    ),
    (  # double win test
        0,
        [
            (0, "d5", 0),
            (1, "d5", 0),
        ],
        2,
    ),
    (  # overthrow test
        0,
        [
            (0, "10", 0),
        ],
        1,
    ),
    (  # overthrow, win test
        0,
        [
            (0, "10", 0),
            (1, "d5", 0),
        ],
        2,
    ),
    (  # win, overthrow test
        0,
        [
            (0, "d5", 0),
            (1, "10", 0),
        ],
        2,
    ),
]


@pytest.mark.parametrize("start_player, throws, current_player", current_player_if_data)
def test_current_player_if_finished(
    start_player: int, throws: list[tuple[int, str, int]], current_player: int
) -> None:
    game_options = GameOptions(
        start_player=start_player,
        sets=1,
        legs=1,
        start_points=10,
        input_method=InputMethod.THREEDARTS,
    )
    scoreboard = Scoreboard(game_options)
    for player in ["a", "b", "c"]:
        scoreboard.register_player(player)
    players = scoreboard.get_players()
    for player_id, throw, dart in throws:
        scoreboard.add_throw(players[player_id], Throw(throw), dart)
    print(scoreboard.get_history())
    assert (
        scoreboard.current_player_and_throw()[0]
        == scoreboard.get_players()[current_player]
    )


IS_OVERTHROW = True
straight_out_data: list[tuple[str, int, bool]] = [
    ("12", 0, not IS_OVERTHROW),
    ("d6", 0, not IS_OVERTHROW),
    ("t4", 0, not IS_OVERTHROW),
    ("11", 1, not IS_OVERTHROW),
    ("d5", 2, not IS_OVERTHROW),
    ("13", 12, IS_OVERTHROW),
    ("d7", 12, IS_OVERTHROW),
]


@pytest.mark.parametrize(
    "last_throw, remaining_score, _",
    straight_out_data,
)
def test_subtract_straight_out(
    last_throw: str,
    remaining_score: int,
    _: bool,
) -> None:
    game_options = GameOptions(
        check_out=CheckInOut.STRAIGHT,
        sets=1,
        legs=1,
        start_points=12,
    )
    scoreboard = Scoreboard(game_options)
    player = scoreboard.register_player("player")
    scoreboard.add_throw(player, Throw(last_throw), 0)
    assert scoreboard.get_remaining_score_of(player) == remaining_score


@pytest.mark.parametrize(
    "last_throw, _, result",
    straight_out_data,
)
def test_is_overthrow_straight_out(
    last_throw: str,
    _: int,
    result: bool,
) -> None:
    game_options = GameOptions(
        check_out=CheckInOut.STRAIGHT,
        sets=1,
        legs=1,
        start_points=12,
    )
    scoreboard = Scoreboard(game_options)
    player = scoreboard.register_player("player")
    remaining_score = scoreboard.get_remaining_score_of(player)
    assert (
        is_overthrow(remaining_score, Throw(last_throw), game_options.check_out)
        == result
    )


double_out_data: list[tuple[int, str, int, bool]] = [
    (12, "d6", 0, not IS_OVERTHROW),
    (12, "12", 12, IS_OVERTHROW),
    (12, "d7", 12, IS_OVERTHROW),
    (12, "13", 12, IS_OVERTHROW),
    (12, "11", 12, IS_OVERTHROW),
    (12, "d5", 2, not IS_OVERTHROW),
    (11, "11", 11, IS_OVERTHROW),
    (11, "12", 11, IS_OVERTHROW),
    (11, "d6", 11, IS_OVERTHROW),
    (11, "13", 11, IS_OVERTHROW),
]


@pytest.mark.parametrize(
    "start_points, last_throw, remaining_score, _",
    double_out_data,
)
def test_subtract_double_out(
    start_points: int,
    last_throw: str,
    remaining_score: int,
    _: bool,
) -> None:
    game_options = GameOptions(
        check_out=CheckInOut.DOUBLE,
        sets=1,
        legs=1,
        start_points=start_points,
    )
    scoreboard = Scoreboard(game_options)
    player = scoreboard.register_player("player")
    scoreboard.add_throw(player, Throw(last_throw), 0)
    assert scoreboard.get_remaining_score_of(player) == remaining_score


@pytest.mark.parametrize(
    "start_points, last_throw, _, result",
    double_out_data,
)
def test_is_overthrow_double_out(
    start_points: int,
    last_throw: str,
    _: int,
    result: bool,
) -> None:
    game_options = GameOptions(
        check_out=CheckInOut.DOUBLE,
        sets=1,
        legs=1,
        start_points=start_points,
    )
    scoreboard = Scoreboard(game_options)
    player = scoreboard.register_player("player")
    remaining_score = scoreboard.get_remaining_score_of(player)
    assert (
        is_overthrow(remaining_score, Throw(last_throw), game_options.check_out)
        == result
    )


is_win_data: list[tuple[str, int, bool]] = [
    ("leg", 0, False),
    ("leg", 1, False),
    ("leg", 2, True),
    ("set", 0, False),
    ("set", 1, False),
    ("set", 2, True),
    ("set", 3, False),
    ("set", 4, True),
    ("game", 0, False),
    ("game", 1, False),
    ("game", 2, False),
    ("game", 3, False),
    ("game", 4, True),
]


@pytest.mark.parametrize(
    "asked, throws_to_input, result",
    is_win_data,
)
def test_is_win(
    asked: str,
    throws_to_input: int,
    result: bool,
) -> None:
    game_options = GameOptions(
        check_out=CheckInOut.DOUBLE,
        sets=2,
        legs=1,
        start_points=20,
    )
    scoreboard = Scoreboard(game_options)
    player = scoreboard.register_player("player")
    for i, dart in enumerate(range(throws_to_input)):
        player, throw_in_round = scoreboard.current_player_and_throw()
        scoreboard.add_throw(player, Throw("d5"), throw_in_round)
        if (i + 1) % 2 == 0:
            # condition for leg and set needs to be checked before
            # appending to history, continue on last
            if asked != "game" and throws_to_input - 1 == i:
                continue
            scoreboard.history.append([])
            scoreboard.history[-1].append([])
    assert scoreboard.is_win(asked, player) == result
