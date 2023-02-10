from typing import Optional
from dataclasses import dataclass
from src.game_options import GameOptions, CheckInOut
from src.throw import Throw


@dataclass
class Player:
    idf: int
    name: str


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
    player: Player
    round_of_leg: int
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
    def __init__(self, game_options: GameOptions):
        self.game_options = game_options
        self.players: list[Player] = []
        self.history: list[list[list[Turn]]] = [[[]]]

    def register_player(self, name: str) -> Player:
        player = Player(len(self.players), name)
        self.players.append(player)
        return player

    def add_throw(self, player: Player, throw: Throw, throw_in_round: int) -> None:
        self.history[-1][-1].append(
            Turn(
                player=player,
                round_of_leg=self.get_round(player),
                score=self.get_remaining_score_of(player),
                throw=throw,
                throw_in_round=throw_in_round,
            )
        )

    def start_player_of_leg(
        self,
    ) -> Player:
        number_of_player_shifts = self.game_options.start_player
        for player in self.players:
            number_of_player_shifts += self.get_won_sets_of(player)
            number_of_player_shifts += self.get_won_legs_of(player)
        return self.players[number_of_player_shifts % len(self.players)]

    def current_player_and_throw(self) -> tuple[Player, int]:
        last_turn = next(
            reversed(self.history[-1][-1]),
            None,
        )
        start_player = self.start_player_of_leg()
        if not last_turn:
            return start_player, 0
        if (
            last_turn.throw_in_round < self.game_options.input_method.value - 1
            and not self.was_overthrow(last_turn.player)
            and self.get_remaining_score_of(last_turn.player)
        ):
            return last_turn.player, last_turn.throw_in_round + 1
        count = 1
        while True:
            next_id = (self.players.index(last_turn.player) + count) % len(self.players)
            if self.get_remaining_score_of(self.players[next_id]):
                break
            if count >= len(self.players):
                raise ValueError("No player with score different from zero found")
            count += 1
        return self.players[next_id], 0

    def was_overthrow(self, player: Player) -> bool:
        last_turn = self.get_last_turn_of_leg(player)
        if not last_turn:
            return False
        return is_overthrow(
            last_turn.score, last_turn.throw, self.game_options.check_out
        )

    def append_hist_if_leg_finished(self) -> tuple[bool, Optional[Player]]:
        if self.number_of_remaining_players() > 1 and len(self.players) > 1:
            return False, None
        winner = self.find_winner_of_leg()
        if self.is_win("leg", winner):
            if self.is_win("set", winner):
                self.history.append([])
            self.history[-1].append([])
            return True, winner
        return False, None

    def find_winner_of_leg(self, dset: int = -1, leg: int = -1) -> Player:
        if len(self.players) == 1:
            return self.players[0]
        for turn in self.history[dset][leg]:
            if not subtract(turn.score, turn.throw, self.game_options.check_out):
                return turn.player
        raise ValueError("Called on an unfinished leg")

    def is_win(self, asked: str, player: Player) -> bool:
        if asked == "leg":
            return self.get_remaining_score_of(player) == 0
        elif asked == "set":
            return self.get_won_legs_of(player) >= self.game_options.legs
        elif asked == "game":
            return self.get_won_sets_of(player) >= self.game_options.sets
        raise ValueError(f"Cannot determine if is_win() with input '{asked}'")

    def number_of_remaining_players(self) -> int:
        count = 0
        for player in self.players:
            if self.get_remaining_score_of(player):
                count += 1
        return count

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

    def get_players(self) -> list[Player]:
        return self.players

    def get_last_turn_of_leg(self, player: Player) -> Optional[Turn]:
        last_turn = next(
            (turn for turn in reversed(self.history[-1][-1]) if turn.player == player),
            None,
        )
        return last_turn

    def get_remaining_score_of(self, player: Player) -> int:
        last_turn = self.get_last_turn_of_leg(player)
        if not last_turn:
            return self.game_options.start_points
        return subtract(last_turn.score, last_turn.throw, self.game_options.check_out)

    def get_round(self, player: Player) -> int:
        last_turn = self.get_last_turn_of_leg(player)
        if not last_turn:
            return 0
        if (
            last_turn.throw_in_round >= self.game_options.input_method.value - 1
            or self.was_overthrow(last_turn.player)
        ):
            return last_turn.round_of_leg + 1
        return last_turn.round_of_leg

    def get_turns_of_round(
        self, round_of_leg: int, dset: int = -1, leg: int = -1
    ) -> list[Turn]:
        turns: list[Turn] = []
        for turn in self.history[dset][leg]:
            if turn.round_of_leg == round_of_leg:
                turns.append(turn)
        return turns

    # probably separate to statistics class
    def get_won_sets_of(self, player: Player) -> int:
        won_sets = 0
        for i, dset in enumerate(self.history):
            if not len(dset[0]):
                continue
            if self.get_won_legs_of(player, i) >= self.game_options.legs:
                won_sets += 1
        return won_sets

    def get_won_legs_of(self, player: Player, dset: int = -1) -> int:
        won_legs = 0
        for leg in self.history[dset]:
            if not len(leg):
                continue
            for turn in leg:
                if not subtract(turn.score, turn.throw, self.game_options.check_out):
                    if turn.player == player:
                        won_legs += 1
                    break
        return won_legs

    def average_darts_of(self, player: Player) -> tuple[float, int]:
        darts = 0
        thrown_total = 0
        for dset in self.history:
            for leg in dset:
                for turn in leg:
                    if not turn.player == player:
                        continue
                    if not is_overthrow(
                        turn.score, turn.throw, self.game_options.check_out
                    ):
                        thrown_total += turn.throw.calc_score()
                        darts += 1
                    else:
                        darts += (
                            self.game_options.input_method.value - turn.throw_in_round
                        )
        if not darts:
            return 0, darts
        return thrown_total / darts * 3, darts

    def get_all_stats(self) -> list[Stats]:
        all_stats = []
        for player in self.players:
            average, thrown_darts = self.average_darts_of(player)
            player_stats = Stats(
                player=player.name,
                sets=self.get_won_sets_of(player),
                legs=self.get_won_legs_of(player),
                score=self.get_remaining_score_of(player),
                average=average,
                darts=thrown_darts,
            )
            all_stats.append(player_stats)
        return all_stats
