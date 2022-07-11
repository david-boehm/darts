from src.game_options import GameOptions, GameMode
from src.scoreboard import Scoreboard
from src.cli import CLI


class Darts():
	def __init__(self, ui:CLI , players: list[str], game_opt: GameOptions) -> None:
		self.ui = ui
		self.scoreboard = Scoreboard(game_opt)
		self.players = players
		self.game_opt = game_opt
		# self.ui.write(f"players found: {self.players}")
		# self.ui.write(f"Game options {self.game_opt}")
	
	def play(self) -> None:
		self.ui.display_game_options(self.game_opt)
		self.ui.write("--- Game on! ---")
		if self.game_opt.game_mode == GameMode.X01:
			game_won = False
			for player in self.players:
				self.scoreboard.register_player(player)
			self.ui.display_scoreboard(*self.scoreboard.get_won_sets_and_legs(), 
				self.scoreboard.get_remaining_score(),False)
			while not game_won:
				game_won = self.do_X01_round()
				self.ui.display_scoreboard(*self.scoreboard.get_won_sets_and_legs(), 
					self.scoreboard.get_remaining_score())

	def do_X01_round(self) -> bool:
		for player in set_start_player(self.players, self.game_opt.start_player, *self.scoreboard.get_won_sets_and_legs()):
			self.ui.write(f"\nDarts of {player} - (prefix d for double or t for tripple + Number, eg t20): ")
			for dart in range(self.game_opt.input_method.value):
				game_win, set_win, leg_win = False, False, False
				throw = self.ui.read_throw(f"{player} requires: {self.scoreboard.get_remaining_score_of_player(player)} - Dart {dart+1}: ")
				remaining_score = self.scoreboard.get_remaining_score_of_player(player)

				if remaining_score - throw.calc_score() == 0: 
					leg_win = True
					if self.scoreboard.get_won_legs_of_player(player) + 1 >= self.game_opt.legs:
						set_win, leg_win = True, True
						if self.scoreboard.get_won_sets_of_player(player) + 1 >= self.game_opt.sets:
							game_win = True
					self.scoreboard.add_throw(player, throw, set_win, leg_win)
					return game_win

				self.scoreboard.add_throw(player, throw, False, False)
				if remaining_score - throw.calc_score() < 0:
					self.ui.overthrow()
					break

		return False

def set_start_player(players: list[str], start_player: int, sets: dict[str,int], legs: dict[str,int]) -> list[str]:
	# sets, legs = self.scoreboard.get_won_sets_and_legs()
	shift_legs = sum(legs.values()) % len(players)
	shift_sets = sum(sets.values()) % len(players)
	# if shift_sets + shift_legs + start_player == len(players):
	# 	return players
	rotated_players = players.copy()
	for i in range((shift_sets + shift_legs + start_player)%len(players)):
		rotated_players.append(rotated_players.pop(0))
	return rotated_players

def main() -> None:
	ui = CLI()
	players = ui.read_players()
	game_opt = ui.read_game_options(players)
	game = Darts(ui, players, game_opt)
	game.play()

if __name__ == "__main__":
	main()