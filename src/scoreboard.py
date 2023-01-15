from typing import Optional, Union
from dataclasses import dataclass
from src.game_options import GameOptions, CheckInOut
from src.general.throw import Throw

Num = Union[int, float]


@dataclass
class Stats:
    player: str
    sets: int = 0
    legs: int = 0
    score: int = 0
    average: float = 0
    darts: int = 0


@dataclass
class Turn:
    player: str
    score: int
    throw: Throw
    won_sets: int = 0
    won_legs: int = 0
    leg_breaks: int = 0
    set_breaks: int = 0


class Scoreboard:
    def __init__(self, game_opt: GameOptions):
        self.game_opt = game_opt
        self.players: list[str] = []
        self.won_legs: dict[str, int] = {}
        self.won_sets: dict[str, int] = {}
        self.history: list[list[list[Turn]]] = [[[]]]
        self.where_leg_won: list[int] = [0]

    def register_player(self, player: str) -> None:
        self.players.append(player)
        self.won_legs[player] = 0
        self.won_sets[player] = 0

    def add_throw(self, player: str, throw: Throw) -> None:
        self.history[-1][-1].append(
            Turn(
                player=player,
                score=self.get_remaining_score_of(player),
                throw=throw,
                won_sets=self.won_sets[player],
                won_legs=self.won_legs[player],
            )
        )
        if self.is_win("leg", player):
            self.where_leg_won.append(len(self.history) + 1)
            self.history[-1].append([])
            self.won_legs[player] += 1
        if self.is_win("set", player):
            self.history.append([[]])
            self.reset_legs()
            self.won_sets[player] += 1

    def is_win(self, asked: str, player: str) -> bool:
        if asked == "leg":
            return self.get_remaining_score_of(player) == 0
        elif asked == "set":
            return self.get_won_legs_of(player) >= self.game_opt.legs
        elif asked == "game":
            return self.get_won_sets_of(player) >= self.game_opt.sets
        raise ValueError(f"Cannot determine if is_win() with input '{asked}'")

    def undo_throw(self) -> bool:
        if (
            not len(self.history[-1][-1])
            and len(self.history[-1]) == 1
            and len(self.history) == 1
        ):
            return False
        if not len(self.history[-1][-1]):
            self.history[-1].pop()
        if not len(self.history[-1]):
            self.history.pop()
        self.history[-1][-1].pop()
        return True

    def reset_legs(self) -> None:
        for player in [*self.won_legs]:
            self.won_legs[player] = 0

    def get_history(self) -> list[list[list[Turn]]]:
        return self.history

    def get_last_turn_of_leg(self, player: str) -> Optional[Turn]:
        last_turn = next(
            (turn for turn in reversed(self.history[-1][-1]) if turn.player == player),
            None,
        )
        return last_turn

    def get_remaining_score_of(self, player: str) -> int:
        last_turn = self.get_last_turn_of_leg(player)
        if not last_turn:
            return self.game_opt.start_points
        return self.subtract(last_turn.score, last_turn.throw)
        raise ValueError("Could not calculate remaining score")

    def get_won_sets_of(self, player: str) -> int:
        won_sets = 0
        for i, dset in enumerate(self.history):
            if not len(dset[0]):
                continue
            if self.get_won_legs_of(player, i) >= self.game_opt.legs:
                won_sets += 1
        return won_sets

    def get_won_legs_of(self, player: str, dset: int = -1) -> int:
        won_legs = 0
        for leg in self.history[dset]:
            if not len(leg):
                continue
            if leg[-1].player == player and not self.subtract(
                leg[-1].score, leg[-1].throw
            ):
                won_legs += 1
        return won_legs

    def get_won_sets_and_legs(self) -> tuple[dict[str, int], dict[str, int]]:
        return {player: self.get_won_sets_of(player) for player in self.players}, {
            player: self.get_won_legs_of(player) for player in self.players
        }

    def get_won_sets_and_legs_of_player(self, player: str) -> tuple[int, int]:
        return self.get_won_sets_of(player), self.get_won_legs_of(player)

    def subtract(self, score: int, throw: Throw) -> int:
        # subtracting with respect to the chosen game options
        prefix, _ = throw.get_and_strip_prefix()
        remaining = score - throw.calc_score()
        if remaining < 0:
            return score
        elif remaining == 0:
            if self.game_opt.check_out == CheckInOut.DOUBLE:
                if prefix != "d":
                    return score
            elif self.game_opt.check_out != CheckInOut.STRAIGHT:
                raise NotImplementedError("Checkoutmethod not implemented")
        return remaining

    def calc_average_of(self, player: str) -> float:
        darts = 0
        thrown_total = 0
        for dset in self.history:
            for leg in dset:
                for turn in leg:
                    if not turn.player == player:
                        continue
                    thrown_total += turn.throw.calc_score()
                    darts += 1
        if not darts:
            return 0
        return thrown_total / darts

    def get_all_stats(self) -> list[Stats]:
        all_stats = []
        for player in self.players:
            player_stats = Stats(
                player=player,
                sets=self.get_won_sets_of(player),
                legs=self.get_won_legs_of(player),
                score=self.get_remaining_score_of(player),
                average=self.calc_average_of(player),
            )
            all_stats.append(player_stats)
        return all_stats
