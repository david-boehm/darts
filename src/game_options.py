from enum import Enum, auto
from dataclasses import dataclass

SEGMENTS = [x for x in range(26) if x <= 20 or x == 25]
IMPOSSIBLE_SCORES = [163, 166, 169, 172, 173, 175, 176, 178, 179]
BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]

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

@dataclass
class GameOptions:
	game_mode: GameMode
	sets: int
	legs: int
	start_points: int
	check_out: CheckInOut
	check_in: CheckInOut
	win_mode: SetLegMode
	input_method: InputMethod
