import os, sys
from src.game_options import GameOptions, GameMode, CheckInOut, SetLegMode, InputMethod
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

	def display_game_options(self, game_opt: GameOptions) -> None:
		dashes = 15
		print(dashes*"#" + " Game settings " + dashes*"#")
		for key, value in game_opt.__dict__.items():
			print(f"{key}: {value}")
		# print(game_opt)
		print((2*dashes+15)*"#")

	def overthrow(self) -> None:
		self.write("Overthrow")

	def read_players(self) -> list[str]:
		to_parse = input("Players (sep by whitespace): ")
		return to_parse.split()

	def read_game_options(self) -> GameOptions:
		game_opt = GameOptions(
			game_mode = GameMode.X01,
			sets = 1,
			legs = 2,
			start_points = 501,
			check_out = CheckInOut.DOUBLE,
			check_in = CheckInOut.STRAIGHT,
			win_mode = SetLegMode.FIRSTTO,
			input_method = InputMethod.THREEDARTS
			)
		return game_opt

	def read_throw(self, message: str) -> Throw:
		while True:
			try:
				user_input = input(message)
				if user_input.lower() in ABORT_MSG:
					break
				throw = Throw(user_input)
				throw.is_valid_input()
				return throw
			except ValueError as err:
				print(f"Wrong input: {err}")
		sys.exit(f"Game was aborted via command: {user_input}")  
