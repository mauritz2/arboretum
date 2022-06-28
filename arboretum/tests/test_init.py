import pytest
from arboretum import Board, Player

@pytest.fixture
def board():
	return Board(5, 2)

@pytest.fixture
def player():
	return Player()


def test_create_empty_board_grid(board):
	assert(len(board.board_grid) == 5)


def test_place_tree(board, player):
	player.place_tree(board, (0,1))
	assert board.board_grid[0][1] == "[X]"
