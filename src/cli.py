import sys
from typing import Optional
from platform import system
import colorama

from src.scoreboard import Stats, Turn, subtract
from src.game_options import (
    GameOptions,
    InputMethod,
    ThrowReturn,
    load_game_opt_from_file,
)
from src.general.throw import Throw

ABORT_MSG = ["exit", "abort", "quit", "stop", "end"]
UNDO = ["undo", "back"]
IMPLEMENTED_OS = {"Windows": "cls", "Linux": "clear"}
STATS_TO_PRINT = ["player", "sets", "legs", "score", "average", "darts"]


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
        colorama.just_fix_windows_console()
        self.cmd_clear = get_console_clear()
        self.lines_to_delete = 0

    def write(self, line: str, increment_lines: int = 1) -> None:
        self.lines_to_delete += increment_lines
        print(line)

    def read(self, line: str, increment_lines: int = 1) -> str:
        self.lines_to_delete += increment_lines
        return input(line)

    def display_game_start(self, game_opt: GameOptions) -> None:
        self.display_game_options(game_opt)
        self.write("--- Game on! ---")

    def display_input_help(self, input_method: InputMethod) -> None:
        if input_method == InputMethod.THREEDARTS:
            msg = (
                "\n(prefix d for double or t for triple + Number, eg t20,\n"
                "enter 'undo' to undo last entered throw, \n"
                "enter 'exit' or 'quit' to stop the game)\n"
            )
        else:
            raise NotImplementedError("Input method '{input_method}' not supported")
        self.write(msg, 5)

    def display_scoreboard(
        self,
        statistics: list[Stats],
        last_turns: list[Turn],
        game_opt: GameOptions,
        clear_screen: bool = True,
    ) -> None:
        if clear_screen:
            for _ in range(self.lines_to_delete + 1):
                sys.stdout.write("\033[2K")  # clear line
                sys.stdout.write("\033[F")  # back to previous line
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
        self.display_input_help(game_opt.input_method)
        for turn in reversed(last_turns):
            previous_turn = (
                f"{turn.player} requires: {turn.score}"
                f" - Dart {turn.throw_in_round+1}: {turn.throw.input_score}"
            )
            _, is_overthrow = subtract(turn.score, turn.throw, game_opt.check_out)
            if is_overthrow:
                previous_turn += "  - Overthrow"
            self.write(previous_turn)

    def display_game_options(self, game_opt: GameOptions) -> None:
        dashes = 15
        self.write(dashes * "#" + " Game settings " + dashes * "#")
        for key, value in game_opt.__dict__.items():
            self.write(f"{key}: {value}")
        self.write((2 * dashes + 15) * "#")
        self.read("If options read press enter")

    def read_throw(
        self, player: str, remaining_score: int, dart: int
    ) -> tuple[ThrowReturn, Throw]:
        while True:
            user_input = self.read(
                f"{player} requires: {remaining_score} - Dart {dart+1}: "
            )
            if user_input.lower() in ABORT_MSG:
                return ThrowReturn.EXIT, Throw("0")
            elif user_input.lower() in UNDO:
                return ThrowReturn.UNDO, Throw("0")
            try:
                throw = Throw(user_input)
                return ThrowReturn.THROW, throw
            except ValueError as err:
                self.write(f"Wrong input: {err}")

    def read_players(self) -> list[str]:
        to_parse = self.read("Players (sep by whitespace, leave blank to exit): ")
        return to_parse.split()

    def read_game_options(self, players: list[str]) -> GameOptions:
        start_player = 0
        while len(players) > 1:
            self.write("Select starting player with number:")
            to_display = ""
            for i, name in enumerate(players):
                to_display += f"{i+1}: {name}"
                if i < len(players) - 1:
                    to_display += "  -  "
            to_display += ": "
            player_number = self.read(to_display)
            try:
                start_player = int(player_number) - 1
            except ValueError:
                self.write("Input was not a integer")
                continue
            if len(players) > start_player >= 0:
                break
            self.write("Selected player not valid")

        game_opt = load_game_opt_from_file()
        game_opt.start_player = start_player
        game_opt.save_to_file()
        return game_opt
