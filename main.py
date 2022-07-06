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

			sets, legs = self.scoreboard.get_sets_and_legs()
			while not game_won:
				self.ui.display_scoreboard(sets, legs, self.scoreboard.get_points())
				game_won = self.do_X01_turn()
				sets, legs = self.scoreboard.get_sets_and_legs()
			self.ui.display_scoreboard(sets, legs, self.scoreboard.get_points(),False)

	def do_X01_turn(self) -> bool:
		for player in self.players:
			self.ui.write(f"\nDarts of {player} - (prefix d for double or t for tripple + Number, eg t20): ")
			for dart in range(self.game_opt.input_method.value):
				throw = self.ui.read_throw(f"{player} requires: {self.scoreboard.get_points_of_player(player)} - Dart {dart+1}: ")
				overthrow = self.scoreboard.subtract_score(player, throw.calc_score(), dart)
				# for turn in self.scoreboard.get_history():
				# 	print(turn)
				if overthrow:
					self.ui.overthrow()
					break
				else: 
					leg_win = self.scoreboard.check_if_leg_win(player)
					set_win = self.scoreboard.check_if_set_win(player)
					game_win = self.scoreboard.check_if_game_win(player)
					if leg_win:
						 return (leg_win and game_win)
		return False

def main() -> None:
	ui = CLI()
	players = ui.read_players()
	game_opt = ui.read_game_options()
	game = Darts(ui, players, game_opt)
	game.play()

if __name__ == "__main__":
	main()