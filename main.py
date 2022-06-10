import os
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

class CLI():
	def __init__(self) -> None:
		pass

	def write(self, message: str) -> None:
		print(f"{message}")

	def display_scoreboard(self, sets: dict[str, int], legs: dict[str, int], points: dict[str, int], clear_screen: bool = True) -> None:
		if clear_screen:
			os.system('cls')
		dashes = 10
		print(dashes*"-" + " Scoreboard " + dashes*"-")
		print("Name\tSets\tLegs\tPoints")
		for player in [*sets]:
			print(f"{player}:\t{sets[player]}\t{legs[player]}\t{points[player]}")
		print((2*dashes+12)*"-")

	def display_game_options(self, game_opt: dict[str, int]) -> None:
		dashes = 15
		print(dashes*"-" + " Game settings " + dashes*"-")
		for key,value in game_opt.items():
			print(f"{key}: {value}")
		print((2*dashes+15)*"-")

	def overthrow(self) -> None:
		self.write("Overthrow")

	def read_players(self) -> list[str]:
		to_parse = input("Players (sep by whitespace): ")
		return to_parse.split()

	def read_game_options(self) -> dict[str,int]:
		game_opt = {}
		game_opt["game_mode"] = GameMode.X01
		game_opt["start_points"] = 501
		game_opt["sets"] = 1
		game_opt["legs"] = 2
		game_opt["check_out"] = CheckInOut.DOUBLE
		game_opt["check_in"] = CheckInOut.STRAIGHT
		game_opt["mode"] = SetLegMode.FIRSTTO
		game_opt["input_method"] = InputMethod.THREEDARTS
		return game_opt

	def read_score(self, message) -> int:
		while True:
			try:
				dart = input(message)
				if len(dart.split()) != 1:
					raise ValueError(f"Number of input darts: {len(dart.split())} not equal to 1")
				if dart.isdecimal():
					return int(dart)
				elif dart.lower() == "exit":
					exit()
				else:
					if dart.lower().startswith("d"):
						return int(dart[1:])*2
					elif dart.lower().startswith("t"):
						return int(dart[1:])*3
					else:
						raise ValueError(f"Input does not match expected pattern")
			except ValueError as err:
				print(f"Wrong input: {err}")

class Scoreboard():
	def __init__(self, game_opt: dict[str,int]):
		self.game_opt = game_opt
		self.points: dict[str, int] = {}
		self.won_legs: dict[str, int] = {}
		self.won_sets: dict[str, int] = {}

	def register_player(self, player: str) -> None:
		self.points[player] = self.game_opt["start_points"]
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
		if self.won_legs[player] >= self.game_opt["legs"]:
			self.reset_legs()
			self.won_sets[player] += 1
			return True
		return False

	def check_if_game_win(self, player: str) -> bool:
		if self.won_sets[player] >= self.game_opt["sets"]:
			return True
		return False

	def reset_points(self) -> None:
		for player in [*self.points]:
			self.points[player] = self.game_opt["start_points"]

	def reset_legs(self) -> None:
		for player in [*self.won_legs]:
			self.won_legs[player] = 0

	def get_points(self, player: str = None) -> dict[str, int]:
		if player:
			return self.points[player]
		return self.points

	def get_sets_and_legs(self, player: str = None) -> (dict[str, int], dict[str, int]):
		if player:
			return self.won_sets[player], self.won_legs[player]
		return self.won_sets, self.won_legs

class Darts():
	def __init__(self, ui:CLI , players: list[str], game_opt: dict[str,int]) -> None:
		self.ui = ui
		self.scoreboard = Scoreboard(game_opt)
		self.players = players
		self.game_opt = game_opt
		# self.ui.write(f"players found: {self.players}")
		# self.ui.write(f"Game options {self.game_opt}")
	
	def play(self) -> None:
		self.ui.display_game_options(self.game_opt)
		self.ui.write("--- Game on! ---")
		if self.game_opt["game_mode"] == GameMode.X01:
			game_won = False
			for player in self.players:
				self.scoreboard.register_player(player)

			sets, legs = self.scoreboard.get_sets_and_legs()
			self.ui.display_scoreboard(sets, legs, self.scoreboard.get_points(),False)
			while not game_won:
				game_won = self.do_X01_turn()
				sets, legs = self.scoreboard.get_sets_and_legs()
				self.ui.display_scoreboard(sets, legs, self.scoreboard.get_points())

	def do_X01_turn(self) -> None:
		for player in self.players:
			self.ui.write(f"\nDarts of {player} - (prefix d for double or t for tripple + Number, eg t20): ")
			for dart in range(self.game_opt["input_method"].value):
				score = self.ui.read_score(f"{player} requires: {self.scoreboard.get_points(player)} - Dart {dart+1}: ")
				overthrow = self.scoreboard.subtract_score(player, score, dart)
				if overthrow:
					self.ui.overthrow()
					break
				else: 
					leg_win = self.scoreboard.check_if_leg_win(player)
					set_win = self.scoreboard.check_if_set_win(player)
					game_win = self.scoreboard.check_if_game_win(player)
					if leg_win:
						 return (leg_win and game_win)

def main() -> None:
	ui = CLI()
	players = ui.read_players()
	game_opt = ui.read_game_options()
	game = Darts(ui, players, game_opt)
	game.play()

if __name__ == "__main__":
	main()