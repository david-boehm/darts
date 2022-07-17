import pytest
from src.game_options import InputMethod
from src.general.throw import Throw

valid_test_data = [
    ("t20",InputMethod.THREEDARTS, 60),
    (" t20",InputMethod.THREEDARTS, 60),
    ("t20 ",InputMethod.THREEDARTS, 60),
    ("d20", InputMethod.THREEDARTS, 40),
    ("T20",InputMethod.THREEDARTS, 60),
    ("D20", InputMethod.THREEDARTS, 40),
    ("20", InputMethod.THREEDARTS, 20),
    ("0",InputMethod.THREEDARTS, 0),
    ("0",InputMethod.ROUND, 0),
    ("180",InputMethod.ROUND, 180)
]
@pytest.mark.parametrize(
    "input_score,input_method,score", valid_test_data)
def test_valid_throw(input_score: str, input_method: InputMethod, score: int) -> None:
    throw = Throw(input_score, input_method)
    assert throw.calc_score() == score

invalid_test_data = [
    ("t 20",InputMethod.THREEDARTS),
    ("d20 10", InputMethod.THREEDARTS),
    ("asdf", InputMethod.THREEDARTS),
    ("18s0", InputMethod.ROUND),
    ("a25", InputMethod.THREEDARTS),
    ("25,5", InputMethod.THREEDARTS),
    ("25.5", InputMethod.THREEDARTS),
    ("t25", InputMethod.THREEDARTS),
    ("23", InputMethod.THREEDARTS),
    ("150", InputMethod.THREEDARTS),
    ("181", InputMethod.ROUND),
    ("179", InputMethod.ROUND)
]
@pytest.mark.parametrize(
    "input_score,input_method", invalid_test_data)
def test_invalid_throw(input_score: str, input_method: InputMethod) -> None:
    with pytest.raises(ValueError):
        Throw(input_score, input_method)
