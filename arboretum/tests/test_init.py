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
	location = (0,1)
	player.place_tree(tree, location)
	assert player.board.board_grid[0][1] == config.DECK_SHORTHANDS[tree]

def test_place_tree_not_in_hand(player):
	tree = "Oak 75"
	location = (0,1)
	with pytest.raises(ValueError):
		player.place_tree(tree, location)

def test_place_same_card_twice(player):
	tree = "Oak 1"
	location = (0,1)
	player.place_tree(tree, location)
	with pytest.raises(ValueError):
		player.place_tree(tree, location)

def test_add_drawn_card_to_hand(player):
	card_to_draw =  player.deck.cards[0]
	player.draw_card()
	assert card_to_draw in player.trees_on_hand 

def test_remove_drawn_card_from_deck(player):
	card_to_draw =  player.deck.cards[0]
	player.draw_card()
	assert card_to_draw not in player.deck.cards 

