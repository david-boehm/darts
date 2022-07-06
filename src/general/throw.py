from src.game_options import InputMethod, IMPOSSIBLE_SCORES, SEGMENTS

class Throw():
	def __init__(self, input_score: str, input_methode: InputMethod = InputMethod.THREEDARTS) -> None:
		self.input_score = input_score.strip()
		self.input_methode = input_methode

	def is_valid_input(self) -> None:
		prefix = ""
		input_score = self.input_score
		if len(input_score.split()) != 1:
			raise ValueError(f"Number of input darts: {len(self.input_score.split())} not equal to 1")
		if not input_score.isdecimal():
			if self.input_methode == InputMethod.ROUND:
				raise ValueError(f"Input {self.input_score} is not decimal")
			elif self.input_methode == InputMethod.THREEDARTS:
				if not input_score.lower().startswith("d") and not input_score.lower().startswith("t"):
					raise ValueError(f"Prefix {self.input_score[:1]} does not exist")
			prefix = input_score[:1]
			input_score = input_score[1:]
		if input_score.isdecimal():
			input_score = int(input_score)
			if self.input_methode == InputMethod.ROUND:
				if input_score in IMPOSSIBLE_SCORES or input_score > 180:
					raise ValueError(f"Input {self.input_score} is impossible to score")
			elif self.input_methode == InputMethod.THREEDARTS:
				if not input_score in SEGMENTS:
					raise ValueError(f"Input {self.input_score} is not a segment")
				if prefix.lower() == "t" and input_score == 25:
					raise ValueError(f"Input {self.input_score} is not a segment")
		else: # fail if rest after prefix is not decimal
			raise ValueError(f"Input {self.input_score} does not match pattern")
	

	def calc_score(self) -> int:
		if self.input_score.isdecimal():
			return int(self.input_score)
		elif self.input_score.lower().startswith("d"):
			return int(self.input_score[1:])*2
		elif self.input_score.lower().startswith("t"):
			return int(self.input_score[1:])*3