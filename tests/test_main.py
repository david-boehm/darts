import pytest
from main import set_start_player

def rotate(players: list[str], rotations: int) -> list[str]:
	_players = players.copy()
	for i in range(rotations):
		_players.append(_players.pop(0))
	return _players

def add_win(dict_to_add: dict[str,int], key_to_add: str, value_to_set: int) -> dict[str,int]:
	_dict_to_add = dict_to_add.copy()
	_dict_to_add[key_to_add] = value_to_set
	return _dict_to_add

players = ['a','b','c']
sets = {'a': 0, 'b': 0, 'c': 0}
legs = {'a': 0, 'b': 0, 'c': 0}


test_data = [
	(players,0,sets,legs,rotate(players,0)),
	(players,1,sets,legs,rotate(players,1)),
	(players,2,sets,legs,rotate(players,2)),
	(players,0,sets,add_win(legs,'a',1),rotate(players,1)),
	(players,0,sets,add_win(legs,'b',2),rotate(players,2)),
	(players,0,sets,add_win(legs,'c',3),rotate(players,3)),
	(players,1,sets,add_win(legs,'a',1),rotate(players,2)),
	(players,1,sets,add_win(legs,'b',2),rotate(players,3)),
	(players,1,sets,add_win(legs,'c',3),rotate(players,4)),
	(players,0,add_win(sets,'a',1),legs,rotate(players,1)),
	(players,0,add_win(sets,'a',1),add_win(legs,'a',1),rotate(players,2)),
	(players,0,add_win(sets,'a',1),add_win(legs,'b',2),rotate(players,3)),
	(players,0,add_win(sets,'a',1),add_win(legs,'c',3),rotate(players,4)),
	(players,1,add_win(sets,'a',1),legs,rotate(players,2)),
	(players,1,add_win(sets,'a',1),add_win(legs,'a',1),rotate(players,3)),
	(players,1,add_win(sets,'a',1),add_win(legs,'b',2),rotate(players,4)),
	(players,1,add_win(sets,'a',1),add_win(legs,'c',3),rotate(players,5)),
]

@pytest.mark.parametrize(
	"players,start_player,sets,legs,rotated_players", test_data)
def test_set_start_player(players: list[str], 
	start_player: int, 
	sets: dict[str,int], 
	legs: dict[str,int], 
	rotated_players: list[str]) -> None:
	assert set_start_player(players, start_player, sets, legs) == rotated_players
