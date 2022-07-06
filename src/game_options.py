from enum import Enum, auto

SEGMENTS = [x+1 for x in range(25) if x+1 <= 20 or x+1 == 25]
IMPOSSIBLE_SCORES = [163, 166, 169, 172, 173, 175, 176, 178, 179]
BOGEY_NUMBERS = [169, 168, 166, 165, 163, 162, 159]

class GameMode(Enum):
	X01 = auto()

	def __repr__(self) -> str:
		return f"{self.name} : {self.value}"

class CheckInOut(Enum):
	STRAIGHT = auto()
	DOUBLE = auto()
	MASTER = auto()

	def __repr__(self) -> str:
		return f"{self.name} : {self.value}"

class SetLegMode(Enum):
	FIRSTTO = auto()
	BESTOF = auto()

	def __repr__(self) -> str:
		return f"{self.name} : {self.value}"

class InputMethod(Enum):
	ROUND = 1
	THREEDARTS = 3

	def __repr__(self) -> str:
		return f"{self.name} : {self.value}"