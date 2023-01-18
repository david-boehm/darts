from typing import Optional
from dataclasses import dataclass
from src.game_options import GameOptions, CheckInOut
from src.general.throw import Throw


@dataclass
class Stats:
    player: str
    sets: int = 0
    legs: int = 0
    score: int = 0
    darts: int = 0
    average: float = 0


@dataclass
class Turn:
    player: str
    score: int
    throw: Throw
    throw_in_round: int = 0


def is_overthrow(score: int, throw: Throw, check_out: CheckInOut) -> bool:
    # subtracting with respect to the chosen game GameOptions
    prefix, _ = throw.get_and_strip_prefix()
    remaining = score - throw.calc_score()
    if remaining < 0:
        return True
    if check_out == CheckInOut.DOUBLE:
        if remaining == 0:
            if prefix != "d":
                return True
        elif remaining == 1:
            return True
    elif check_out != CheckInOut.STRAIGHT:
        raise NotImplementedError("Checkoutmethod not implemented")
    return False


def subtract(score: int, throw: Throw, check_out: CheckInOut) -> int:
    if is_overthrow(score, throw, check_out):
        return score
    return score - throw.calc_score()


class Scoreboard:
    def __init__(self, game_opt: GameOptions):
        self.game_opt = game_opt
        self.players: list[str] = []
        self.history: list[list[list[Turn]]] = [[[]]]

    def register_player(self, player: str) -> None:
        self.players.append(player)

    def add_throw(self, player: str, throw: Throw, throw_in_round: int) -> bool:
        self.history[-1][-1].append(
            Turn(
                player=player,
                score=self.get_remaining_score_of(player),
                throw=throw,
                throw_in_round=throw_in_round,
            )
        )
        if self.is_win("set", player):
            self.history.append([[]])
            return True
        if self.is_win("leg", player):
            self.history[-1].append([])
            return True
        return False

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

    def get_history(self) -> list[list[list[Turn]]]:
        return self.history

    def get_turns_of_leg(
        self, dset: int = -1, leg: int = -1, turns_to_return: int = -1
    ) -> list[Turn]:
        last_turns: list[Turn] = []
        if turns_to_return < 0:
            turns_to_return = len(self.players) * 3 - 1
        reversed_leg_history = iter(reversed(self.history[dset][leg]))
        for _ in range(turns_to_return):
            turn = next(reversed_leg_history, None)
            if not turn:
                break
            last_turns.append(turn)
        return last_turns

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
        return subtract(last_turn.score, last_turn.throw, self.game_opt.check_out)

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

            if leg[-1].player == player and not subtract(
                leg[-1].score, leg[-1].throw, self.game_opt.check_out
            ):
                won_legs += 1
        return won_legs

    def get_won_sets_and_legs(self) -> tuple[dict[str, int], dict[str, int]]:
        return {player: self.get_won_sets_of(player) for player in self.players}, {
            player: self.get_won_legs_of(player) for player in self.players
        }

    def average_darts_of(self, player: str) -> tuple[float, int]:
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
            return 0, darts
        return thrown_total / darts * 3, darts

    def get_all_stats(self) -> list[Stats]:
        all_stats = []
        for player in self.players:
            average, thrown_darts = self.average_darts_of(player)
            player_stats = Stats(
                player=player,
                sets=self.get_won_sets_of(player),
                legs=self.get_won_legs_of(player),
                score=self.get_remaining_score_of(player),
                average=average,
                darts=thrown_darts,
            )
            all_stats.append(player_stats)
        return all_stats
