import os
from definitions import *
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
		game_opt["game_mode"] = GameMode.X01.value
		game_opt["start_points"] = 501
		game_opt["sets"] = 1
		game_opt["legs"] = 2
		game_opt["check_out"] = CheckInOut.DOUBLE.value
		game_opt["check_in"] = CheckInOut.STRAIGHT.value
		game_opt["mode"] = SetLegMode.FIRSTTO.value
		game_opt["input_method"] = InputMethod.THREEDARTS.value
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
