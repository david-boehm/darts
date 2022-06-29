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

class Throw():
	def __init__(self, input_score: str, input_methode: InputMethod = InputMethod.THREEDARTS) -> None:
		self.input_score = input_score
		self.input_methode = InputMethod
		self.score = self.is_valid_input()

	def is_valid_input(self) -> int:
		if self.input_methode == InputMethod.ROUND and not self.input_score.isdecimal():
			raise ValueError(f"Input {self.input_score} is not decimal")
		if len(self.input_score.split()) != 1:
			raise ValueError(f"Number of input darts: {len(self.input_score.split())} not equal to 1")
		if self.input_score.isdecimal():
			return int(self.input_score)
		elif self.input_score.lower() == "exit":
			exit()
		else:
			if self.input_score.lower().startswith("d"):
				return int(self.input_score[1:])*2
			elif self.input_score.lower().startswith("t"):
				return int(self.input_score[1:])*3
			else:
				raise ValueError(f"Input does not match expected pattern")