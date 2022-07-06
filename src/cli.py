import os, sys
from typing import Any
from src.game_options import GameMode, CheckInOut, SetLegMode, InputMethod
from src.general.throw import Throw

ABORT_MSG = ["exit","abort","quit","stop","end"]

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

	def read_game_options(self) -> dict[str, Any]:
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

	def read_throw(self, message: str) -> Throw:
		while True:
			try:
				user_input = input(message)
				if user_input in ABORT_MSG:
					break
				throw = Throw(user_input)
				throw.is_valid_input()
				return throw
			except ValueError as err:
				print(f"Wrong input: {err}")
		sys.exit(f"Game was aborted via command: {user_input}")  
