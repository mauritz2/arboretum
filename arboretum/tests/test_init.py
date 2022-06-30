import pytest
from arboretum import Board, Player, Deck, config

@pytest.fixture
def board():
	return Board(5, 2)

@pytest.fixture
def deck():
	return Deck()

@pytest.fixture
def player(board, deck):
	return Player(deck, board)

def test_create_board_grid(board):
	assert(len(board.board_grid) == 5)

def test_place_tree(player):
	tree = "Oak 1"
	row, column = 0, 1
	player.place_tree(tree, row, column)
	assert player.board.board_grid[0][1] == config.DECK_SHORTHANDS[tree]

def test_place_tree_not_in_hand(player):
	tree = "Oak 75"
	row, column = 0, 1
	with pytest.raises(ValueError):
		player.place_tree(tree, row, column)

def test_place_same_card_twice(player):
	tree = "Oak 1"
	row, column = 0, 1
	player.place_tree(tree, row, column)
	with pytest.raises(ValueError):
		player.place_tree(tree, row, column)

def test_place_card_in_occupied_space(player):
	tree1 = "Oak 1"
	tree2 = "Oak 2"
	row, column = 0, 1
	player.place_tree(tree1, row, column)
	with pytest.raises(ValueError):
		player.place_tree(tree2, row, column)

def test_add_drawn_card_to_hand(player):
	card_to_draw =  player.deck.cards[0]
	player.draw_card()
	assert card_to_draw in player.trees_on_hand 

def test_remove_drawn_card_from_deck(player):
	card_to_draw =  player.deck.cards[0]
	player.draw_card()
	assert card_to_draw not in player.deck.cards 

