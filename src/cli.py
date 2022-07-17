import os
from typing import Optional
from platform import system

from src.game_options import GameOptions, GameMode, CheckInOut, SetLegMode, InputMethod, ThrowReturn
from src.general.throw import Throw

ABORT_MSG = ["exit","abort","quit","stop","end"]
UNDO = ["undo","back"]
IMPLEMENTED_OS = ["Windows","Linux"]
OS_CLEAR = ["cls","clear"]

def get_os() -> Optional(str):
    if system() in IMPLEMENTED_OS:
        return system()
    return None

def get_console_clear() -> str:
    for i, os in enumerate(IMPLEMENTED_OS):
        if system() == os:
            return OS_CLEAR[i]
    raise NotImplementedError(f"{system()} clear cmd not implemented")

class CLI():
	def __init__(self) -> None:
        self.cmd_clear = get_console_clear()

	def write(self, message: str) -> None:
		print(f"{message}")

	def display_scoreboard(self, sets: dict[str, int], legs: dict[str, int], points: dict[str, int], clear_screen: bool = True) -> None:
		if clear_screen:
			os.system(self.cmd_clear)
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

	def read_game_options(self, players: list[str]) -> GameOptions:
		start_player = 0
		while len(players) > 1:
			try:
				to_display = "Which player starts the game\n"
				for i,name in enumerate(players):
					to_display += f"{name}: {i+1}"
					if i < len(players) - 1:
						to_display += " - "
				to_display += ": "
				start_player = int(input(to_display)) - 1
				if start_player >= len(players) or start_player < 0:
					raise ValueError("Not a valid player")
				break
			except ValueError as err:
				print(err)

		game_opt = GameOptions(
			game_mode = GameMode.X01,
			sets = 1,
			legs = 2,
			start_points = 501,
			check_out = CheckInOut.DOUBLE,
			check_in = CheckInOut.STRAIGHT,
			win_mode = SetLegMode.FIRSTTO,
			input_method = InputMethod.THREEDARTS,
			start_player = start_player
			)
		return game_opt

	def read_throw(self, message: str) -> tuple[ThrowReturn,Throw]:
		while True:
			try:
				user_input = input(message)
				if user_input.lower() in ABORT_MSG:
					return ThrowReturn.EXIT , Throw("0")
				elif user_input.lower() in UNDO:
					return ThrowReturn.UNDO, Throw("0")
				throw = Throw(user_input)
				throw.is_valid_input()
				return ThrowReturn.THROW, throw
			except ValueError as err:
				print(f"Wrong input: {err}")

