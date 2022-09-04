import os
import json
from enum import Enum, auto
from dataclasses import dataclass
from dataclasses_json import dataclass_json


SEGMENTS = [x for x in range(26) if x <= 20 or x == 25]
IMPOSSIBLE_SCORES = [163, 166, 169, 172, 173, 175, 176, 178, 179]
BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]

GAME_OPTIONS_SAVE_FILE = "game_opt.json"


class ThrowReturn(Enum):
    THROW = "throw"
    UNDO = "undo"
    EXIT = "exit"


class GameMode(Enum):
    X01 = "X01"

    def __str__(self) -> str:
        return self.value


class CheckInOut(Enum):
    STRAIGHT = "straight"
    DOUBLE = "double"
    MASTER = "master"

    def __repr__(self) -> str:
        return self.value


class SetLegMode(Enum):
    FIRSTTO = "firstto"
    BESTOF = "bestof"

    def __repr__(self) -> str:
        return self.value


class InputMethod(Enum):
    ROUND = 1
    THREEDARTS = 3

    def __repr__(self) -> str:
        return f"{self.name} : {self.value}"


@dataclass_json
@dataclass
class GameOptions:
    game_mode: GameMode = GameMode.X01
    sets: int = 1
    legs: int = 2
    start_points: int = 501
    check_out: CheckInOut = CheckInOut.DOUBLE
    check_in: CheckInOut = CheckInOut.STRAIGHT
    win_mode: SetLegMode = SetLegMode.FIRSTTO
    input_method: InputMethod = InputMethod.THREEDARTS
    start_player: int = 0

    def save_to_file(self) -> None:
        with open(GAME_OPTIONS_SAVE_FILE, "w+") as file:
            file.write(self.to_json())


def load_game_opt_from_file(
        file_name: str = GAME_OPTIONS_SAVE_FILE) -> GameOptions:
    if not os.path.exists(file_name):
        return GameOptions()
    with open(file_name, "r") as file:
        values = json.load(file)
    return GameOptions().from_dict(values)
