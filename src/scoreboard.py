from dataclasses import dataclass
from src.game_options import GameOptions
from src.general.throw import Throw

@dataclass
class Turn:
	current_set: int
	current_leg: int
	player: str
	throw: Throw
	# won_sets: int
	# leg_breaks: int
	# won_legs: int
	# set_breaks: int

class Scoreboard():
	def __init__(self, game_opt: GameOptions):
		self.history = list[Turn]
		self.game_opt = game_opt
		self.points: dict[str, int] = {}
		self.won_legs: dict[str, int] = {}
		self.won_sets: dict[str, int] = {}

	def register_player(self, player: str) -> None:
		self.points[player] = self.game_opt.start_points
		self.won_legs[player] = 0
		self.won_sets[player] = 0

	def subtract_score(self, player: str, score: int, dart: int) -> bool:
		if self.points[player] - score < 0:
			return True
		self.points[player] -= score
		return False
		
	def check_if_leg_win(self, player: str) -> bool:
		if self.points[player] == 0:
			self.reset_points()
			self.won_legs[player] += 1
			return True
		return False

	def check_if_set_win(self, player:str) -> bool:
		if self.won_legs[player] >= self.game_opt.legs:
			self.reset_legs()
			self.won_sets[player] += 1
			return True
		return False

	def check_if_game_win(self, player: str) -> bool:
		if self.won_sets[player] >= self.game_opt.sets:
			return True
		return False

	def reset_points(self) -> None:
		for player in [*self.points]:
			self.points[player] = self.game_opt.start_points

	def reset_legs(self) -> None:
		for player in [*self.won_legs]:
			self.won_legs[player] = 0

	def get_points(self) -> dict[str, int]:
		return self.points

	def get_points_of_player(self, player: str) -> int:
		return self.points[player]

	def get_sets_and_legs(self) -> tuple[dict[str, int], dict[str, int]]:
		return self.won_sets, self.won_legs

	def get_sets_and_legs_of_player(self, player: str) -> tuple[int, int]:
		return self.won_sets[player], self.won_legs[player]

