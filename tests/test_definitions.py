import pytest
from definitions import InputMethod, Throw


# class TestThrowInputs(unittest.TestCase):
# 	def __init__(self, input_score:str, input_method: InputMethod, score: int) -> None:
# 		super(TestThrowInputs, self).__init__()
# 		self.input_score = input_score
# 		self.input_method = input_method
# 		self.score = score

valid_test_data = [
	("t20","InputMethod.THREEDARTS", 60),
	("d20", InputMethod.THREEDARTS, 40),
	("20", InputMethod.THREEDARTS, 20),
	("180",InputMethod.ROUND, 180),
	("18s0",InputMethod.ROUND, 180)
]
@pytest.mark.parametrize(
	"input_score,input_method,score", valid_test_data)
def test_valid_throw(input_score: str, input_method: InputMethod, score: int) -> None:
	assert Throw(input_score, input_method).score == score

# def suite() -> unittest.TestSuite:
# 	suite = unittest.TestSuite()
# 	valid_throw_lst = [
# 		("t20",InputMethod.THREEDARTS, 60),
# 		("d20", InputMethod.THREEDARTS, 40),
# 		("20", InputMethod.THREEDARTS, 20),
# 		("180",InputMethod.ROUND, 180),
# 		("18a0",InputMethod.ROUND, 180)]
# 	for valid_input in valid_throw_lst:
# 		suite.addTest(TestThrowInputs(*valid_input))
# 	return suite

# if __name__ == '__main__':
# 	runner = unittest.TextTestRunner()
# 	runner.run(suite())