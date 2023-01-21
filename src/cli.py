import sys
from typing import Optional
from platform import system
import colorama

from src.scoreboard import Stats, Turn, is_overthrow
from src.game_options import (
    GameOptions,
    InputMethod,
    ThrowReturn,
    load_game_opt_from_file,
)
from src.throw import Throw

ABORT_MSG = ["exit", "abort", "quit", "stop", "end"]
UNDO = ["undo", "back"]
IMPLEMENTED_OS = {"Windows": "cls", "Linux": "clear"}
STATS_TO_PRINT = ["player", "sets", "legs", "score", "average", "darts"]
MAX_LINES_TO_DISPLAY: int = 12


def get_os() -> Optional[str]:
    if system() in IMPLEMENTED_OS:
        return system()
    return None


def get_console_clear() -> str:
    for known_os, clear in IMPLEMENTED_OS.items():
        if system() == known_os:
            return clear
    raise NotImplementedError(f"{system()} clear cmd not implemented")


class CLI:
    def __init__(self) -> None:
        if get_os() == "Windows":
            colorama.just_fix_windows_console()
        self.cmd_clear = get_console_clear()
        self.lines_to_delete = 0

    def write(self, line: str, increment_lines: int = 1) -> None:
        self.lines_to_delete += increment_lines
        print(line)

    def read(self, line: str, increment_lines: int = 1) -> str:
        self.lines_to_delete += increment_lines
        try:
            red_input = input(line)
        except KeyboardInterrupt:
            self.write("")
            sys.exit("The game was canceled")
        return red_input

    def display_game_start(self, game_options: GameOptions) -> None:
        self.display_game_options(game_options)
        self.write("--- Game on! ---")

    def display_input_help(self, input_method: InputMethod) -> None:
        if input_method == InputMethod.THREEDARTS:
            msg = (
                "\n(Prefix d for double or t for triple + Number, eg t20,\n"
                "empty input enters 0\n"
                "enter 'undo' to undo last entered throw, \n"
                "enter 'exit' or 'quit' to stop the game)\n"
            )
        else:
            raise NotImplementedError("Input method '{input_method}' not supported")
        self.write(msg, 6)

    def display_scoreboard(
        self,
        statistics: list[Stats],
        turns_of_round: list[Turn],
        game_options: GameOptions,
        clear_screen: bool = True,
    ) -> None:
        if clear_screen:
            sys.stdout.write("\033[2K")  # clear line
            for _ in range(self.lines_to_delete):
                sys.stdout.write("\033[F")  # back to previous line
                sys.stdout.write("\033[2K")  # clear line
            self.lines_to_delete = 0

        max_name_lenght = 0
        for statistic in statistics:
            if len(statistic.player) > max_name_lenght:
                max_name_lenght = len(statistic.player)
        tabs_after_name = (max_name_lenght // 8) + 1

        header = ""
        for field in statistics[0].__dataclass_fields__:
            if field not in STATS_TO_PRINT:
                continue
            if field == "player":
                header += f"{field.capitalize()}" + "\t" * tabs_after_name
            else:
                header += f"{field.capitalize()}\t"
        max_tabs_in_player_line = header.count("\t")
        player_lines: list[str] = []
        for player_stats in statistics:
            to_print = ""
            for field in player_stats.__dataclass_fields__:
                if field not in STATS_TO_PRINT:
                    continue
                sep = "\t"
                value = getattr(player_stats, field)
                if field == "player":
                    sep = ":" + "\t" * (tabs_after_name - len(value) // 8)
                if field == "average":
                    to_print += f"{value:.2f}" + sep
                    continue
                to_print += f"{value}" + sep
            player_lines.append(to_print)

            if to_print.count("\t") > max_tabs_in_player_line:
                max_tabs_in_player_line = to_print.count("\t")

        title = " Scoreboard "  # needs to be even number
        dashes = (max_tabs_in_player_line * 8 - len(title)) // 2

        self.write(dashes * "-" + title + dashes * "-")
        self.write(header)
        for player in player_lines:
            self.write(player)
        self.write((2 * dashes + len(title)) * "-")
        self.display_input_help(game_options.input_method)
        max_line_for_mode = (
            MAX_LINES_TO_DISPLAY // (4 - game_options.input_method.value)
        ) - 1
        for turn in reversed(turns_of_round[:max_line_for_mode]):
            to_print = (
                f"{turn.player.name} requires: {turn.score:3}"
                f" - Dart {turn.throw_in_round+1}: {turn.throw.input_score:<3}"
            )
            if is_overthrow(turn.score, turn.throw, game_options.check_out):
                to_print += "  - Overthrow"
            self.write(to_print)

    def display_game_options(self, game_options: GameOptions) -> None:
        dashes = 15
        self.write(dashes * "#" + " Game settings " + dashes * "#")
        for key, value in game_options.__dict__.items():
            self.write(f"{key}: {value}")
        self.write((2 * dashes + 15) * "#")
        self.read("If options read press enter")

    def read_throw(
        self, player: str, remaining_score: int, dart: int
    ) -> tuple[ThrowReturn, Throw]:
        while True:
            user_input = self.read(
                f"{player} requires: {remaining_score:3} - Dart {dart+1}: "
            )
            if user_input.lower() in ABORT_MSG:
                return ThrowReturn.EXIT, Throw("0")
            elif user_input.lower() in UNDO:
                return ThrowReturn.UNDO, Throw("0")
            elif not len(user_input):
                user_input = "0"
            try:
                throw = Throw(user_input)
                return ThrowReturn.THROW, throw
            except ValueError as err:
                self.write(f"Wrong input: {err}")

    def read_players(self) -> list[str]:
        players: list[str] = []
        self.write("Enter Players (leave empty to continue):")
        to_parse = "not empty"
        while True:
            to_parse = self.read(f"Player {len(players)+1}: ")
            if not len(to_parse):
                break
            players.append(to_parse)
        return players

    def read_game_options(self, players: list[str]) -> GameOptions:
        start_player = 0
        while len(players) > 1:
            self.write("Select starting player with number (empty for 1):")
            to_display = ""
            for i, name in enumerate(players):
                to_display += f"{i+1}: {name}"
                if i < len(players) - 1:
                    to_display += "  -  "
            to_display += ": "
            player_number = self.read(to_display)
            if not len(player_number):
                start_player = 0
                break
            try:
                start_player = int(player_number) - 1
            except ValueError:
                self.write("Input was not a integer")
                continue
            if len(players) > start_player >= 0:
                break
            self.write("Selected player not valid")

        if len(players) > 1:
            self.write(f"Player {start_player+1} as starting player selceted")
        game_options = load_game_opt_from_file()
        game_options.start_player = start_player
        game_options.save_to_file()
        return game_options
