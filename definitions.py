from enum import Enum, auto

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
