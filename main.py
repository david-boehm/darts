from definitions import GameMode
from scoreboard import Scoreboard
from cli import CLI


class Darts():
	def __init__(self, ui:CLI , players: list[str], game_opt: dict[str,int]) -> None:
		self.ui = ui
		self.scoreboard = Scoreboard(game_opt)
		self.players = players
		self.game_opt = game_opt
		# self.ui.write(f"players found: {self.players}")
		# self.ui.write(f"Game options {self.game_opt}")
	
	def play(self) -> None:
		self.ui.display_game_options(self.game_opt)
		self.ui.write("--- Game on! ---")
		if self.game_opt["game_mode"] == GameMode.X01:
			game_won = False
			for player in self.players:
				self.scoreboard.register_player(player)

			sets, legs = self.scoreboard.get_sets_and_legs()
			self.ui.display_scoreboard(sets, legs, self.scoreboard.get_points(),False)
			while not game_won:
				game_won = self.do_X01_turn()
				sets, legs = self.scoreboard.get_sets_and_legs()
				self.ui.display_scoreboard(sets, legs, self.scoreboard.get_points())

	def do_X01_turn(self) -> None:
		for player in self.players:
			self.ui.write(f"\nDarts of {player} - (prefix d for double or t for tripple + Number, eg t20): ")
			for dart in range(self.game_opt["input_method"].value):
				throw = self.ui.read_throw(f"{player} requires: {self.scoreboard.get_points_of_player(player)} - Dart {dart+1}: ")
				overthrow = self.scoreboard.subtract_score(player, throw.calc_score(), dart)
				if overthrow:
					self.ui.overthrow()
					break
				else: 
					leg_win = self.scoreboard.check_if_leg_win(player)
					set_win = self.scoreboard.check_if_set_win(player)
					game_win = self.scoreboard.check_if_game_win(player)
					if leg_win:
						 return (leg_win and game_win)

def main() -> None:
	ui = CLI()
	players = ui.read_players()
	game_opt = ui.read_game_options()
	game = Darts(ui, players, game_opt)
	game.play()

if __name__ == "__main__":
	main()