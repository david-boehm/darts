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
		for player in self.players:
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

					print("total history")
					for turn in self.scoreboard.get_history()[-2:]:
						print(turn)
					print("leg history")
					# still has entries, shoud not have one
					for turn in self.scoreboard.get_leg_history()[-2:]:
						print(turn)
					print(self.scoreboard.where_leg_won)
					input()
					return game_win

				self.scoreboard.add_throw(player, throw, False, False)
				for turn in self.scoreboard.get_leg_history()[-2:]:
					print(turn)
				if remaining_score - throw.calc_score() < 0:
					self.ui.overthrow()
					break

		return False

def main() -> None:
	ui = CLI()
	players = ui.read_players()
	game_opt = ui.read_game_options()
	game = Darts(ui, players, game_opt)
	game.play()

if __name__ == "__main__":
	main()