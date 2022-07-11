from typing import Optional
from dataclasses import dataclass
from src.game_options import GameOptions
from src.general.throw import Throw

@dataclass
class Turn:
	player: str
	score: int
	throw: Throw
	won_sets: int = 0
	won_legs: int = 0
	leg_breaks: int = 0
	set_breaks: int = 0

	def remaining_score(self):
		if self.score - self.throw.calc_score() < 0:
			return self.score
		return self.score - self.throw.calc_score()

class Scoreboard():
	def __init__(self, game_opt: GameOptions):
		self.history: list[Turn] = []
		self.where_leg_won: list[int] = [0]
		self.players: list[str] = []

		self.game_opt = game_opt
		# self.points: dict[str, int] = {}
		self.won_legs: dict[str, int] = {}
		self.won_sets: dict[str, int] = {}

	def register_player(self, player: str) -> None:
		self.players.append(player)

		# self.points[player] = self.game_opt.start_points
		self.won_legs[player] = 0
		self.won_sets[player] = 0

	def add_throw(self, player: str, throw: Throw, set_win: bool, leg_win: bool) -> None:
		# won_sets = self.get_won_sets_of_player(player)
		# won_legs = self.get_won_legs_of_player(player)
		score = self.get_remaining_score_of_player(player)

		if leg_win:
			self.where_leg_won.append(len(self.history)+1)
			self.won_legs[player] += 1
		if set_win:
			self.reset_legs()
			self.won_sets[player] +=1

		self.history.append(Turn(player = player, 
				score = score,
				throw = throw,
				won_sets = self.won_sets[player],
				won_legs = self.won_legs[player]))
		
	# def add_leg_win(self, player: str) -> None:
	# 	self.won_legs[player] += 1

	# def check_if_set_win(self, player:str) -> bool:
	# 	if self.won_legs[player] >= self.game_opt.legs:
	# 		self.reset_legs()
	# 		self.won_sets[player] += 1
	# 		return True
	# 	return False

	# def check_if_game_win(self, player: str) -> bool:
	# 	if self.won_sets[player] >= self.game_opt.sets:
	# 		return True
	# 	return False

	# def reset_points(self) -> None:
	# 	for player in [*self.points]:
	# 		self.points[player] = self.game_opt.start_points

	def reset_legs(self) -> None:
		for player in [*self.won_legs]:
			self.won_legs[player] = 0

	def get_history(self) -> list[Turn]:
		return self.history

	def get_leg_history(self) -> list[Turn]:
		return self.history[self.where_leg_won[-1]:]

	def get_last_turn_of_player(self, player: str) -> Optional[Turn]:
		last_turn = next((turn for turn in reversed(self.get_history()) if turn.player == player), None)
		return last_turn

	def get_last_turn_of_leg_of_player(self, player: str) -> Optional[Turn]:
		last_turn = next((turn for turn in reversed(self.get_leg_history()) if turn.player == player), None)
		return last_turn

	def get_remaining_score(self) -> dict[str, int]:
		return {player: self.get_remaining_score_of_player(player) for player in self.players}

	def get_remaining_score_of_player(self, player: str) -> int:
		last_turn = self.get_last_turn_of_leg_of_player(player)
		if last_turn:
			return last_turn.remaining_score()
		return self.game_opt.start_points

	def get_won_sets_of_player(self, player: str) -> int:
		# last_turn = self.get_last_turn_of_player(player)
		# if last_turn:
		# 	return last_turn.won_sets
		# return 0
		return self.won_sets[player]

	def get_won_legs_of_player(self, player: str) -> int:
		# last_turn = self.get_last_turn_of_player(player)
		# if last_turn:
		# 	return last_turn.won_legs
		# return 0
		return self.won_legs[player]

	def get_won_sets_and_legs(self) -> tuple[dict[str, int], dict[str, int]]:
		return {player: self.get_won_sets_of_player(player) for player in self.players}, \
		{player: self.get_won_legs_of_player(player) for player in self.players}
		# return self.won_sets, self.won_legs

	def get_won_sets_and_legs_of_player(self, player: str) -> tuple[int, int]:
		return self.get_won_sets_of_player(player), self.get_won_legs_of_player(player)
