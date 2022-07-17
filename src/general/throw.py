from src.game_options import InputMethod, IMPOSSIBLE_SCORES, SEGMENTS


class Throw:
    # Eventually meeds a dart variable to safe the thrown dart 1, 2 or 3
    def __init__(self, input_score: str, input_methode: InputMethod = InputMethod.THREEDARTS) -> None:
        self.input_score = input_score.strip().lower()
        self.input_methode = input_methode
        self.is_valid_input()

    def __repr__(self) -> str:
        list_of_items = [f"{key}: {value}" for key, value in self.__dict__.items()]
        return " ".join(list_of_items)

    def is_valid_input(self) -> None:
        prefix = ""
        stripped_input_score = self.input_score
        if len(self.input_score.split()) != 1:
            raise ValueError(f"Number of input darts: {len(self.input_score.split())} not equal to 1")
        if not self.input_score.isdecimal():
            if self.input_methode == InputMethod.ROUND:
                raise ValueError(f"Input {self.input_score} is not decimal")
            elif self.input_methode == InputMethod.THREEDARTS:
                if not self.input_score.startswith("d") and not self.input_score.startswith("t"):
                    raise ValueError(f"Prefix {self.input_score[:1]} does not exist")
            prefix, stripped_input_score = self.get_and_strip_prefix()
        if stripped_input_score.isdecimal():
            int_score = int(stripped_input_score)
            if self.input_methode == InputMethod.ROUND:
                if int_score in IMPOSSIBLE_SCORES or int_score > 180:
                    raise ValueError(f"Input {self.input_score} is impossible to score")
            elif self.input_methode == InputMethod.THREEDARTS:
                if not int_score in SEGMENTS:
                    raise ValueError(f"Input {self.input_score} is not a segment")
                if prefix == "t" and int_score == 25:
                    raise ValueError(f"Input {self.input_score} is not a segment")
        else: # fail if rest after prefix is not decimal
            raise ValueError(f"Input {self.input_score} does not match pattern")

    def calc_score(self) -> int:
        if self.input_score.isdecimal():
            return int(self.input_score)
        else:
            prefix, stripped_input_score = self.get_and_strip_prefix()
            if prefix == "d":
                return 2*int(stripped_input_score)
            return 3*int(stripped_input_score)


    def get_and_strip_prefix(self) -> tuple[str,str]:
        return self.input_score[:1], self.input_score[1:]