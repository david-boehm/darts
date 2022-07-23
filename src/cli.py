import os
from typing import Optional
from platform import system

from src.scoreboard import Stats
from src.game_options import GameOptions, GameMode, CheckInOut, SetLegMode, InputMethod, ThrowReturn
from src.general.throw import Throw

ABORT_MSG = ["exit","abort","quit","stop","end"]
UNDO = ["undo","back"]
IMPLEMENTED_OS = {"Windows":"cls","Linux":"clear"}

def get_os() -> Optional[str]:
    if system() in IMPLEMENTED_OS:
        return system()
    return None

def get_console_clear() -> str:
    for os, clear in IMPLEMENTED_OS.items():
        if system() == os:
            return clear
    raise NotImplementedError(f"{system()} clear cmd not implemented")

class CLI():
    def __init__(self) -> None:
        self.cmd_clear = get_console_clear()

    def write(self, message: str) -> None:
        print(f"{message}")

    def display_scoreboard(self, stats: list[Stats], clear_screen: bool = True) -> None:
        if clear_screen:
            os.system(self.cmd_clear)
        dashes = 10
        print(dashes*"-" + " Scoreboard " + dashes*"-")
        to_print = ""
        for field in stats[0].__dataclass_fields__:
            to_print += f"{field.capitalize()}\t"
        print(to_print)
        for player in stats:
            to_print = ""
            for field in player.__dataclass_fields__:
                sep = "\t"
                if field == "player":
                    sep =":\t"
                if field == "average":
                    to_print += f"{getattr(player,field):.2f}" + sep
                    continue
                to_print += f"{getattr(player,field)}" + sep
            print(to_print)
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
                to_display = "Select starting player with number: \n"
                for i,name in enumerate(players):
                    to_display += f"{i+1}: {name}"
                    if i < len(players) - 1:
                        to_display += "  -  "
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

