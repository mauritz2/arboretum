import pytest
import pickle
from arboretum import Board, Player, Deck, Scorer, config

@pytest.fixture
def board():
	return Board(5, 2)

@pytest.fixture
def deck():
	return Deck()

@pytest.fixture
def player(board, deck):
	return Player(deck, board)

@pytest.fixture
def player2(board, deck):
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

def test_check_if_occupied_loc(board):
	row = 1
	column = 1
	check_occupied = board._check_if_occupied_loc(row, column)
	assert (check_occupied == False)
	board.board_grid[row][column] = "Oak 1"
	check_occupied = board._check_if_occupied_loc(row, column)
	assert (check_occupied == True)

def test_reject_no_adjacency(player):
	tree = "Oak 2"
	row, column = 0, 1
	player.first_tree_placed = True
	with pytest.raises(ValueError):
		player.place_tree(tree, row, column)

def test_reject_no_adjacency_diagnoal_tree(player):
	tree1 = "Oak 1"
	tree2 = "Oak 2"
	row1, column1 = 0, 0
	row2, column2 = 1,1
	player.place_tree(tree1, row1, column1)
	with pytest.raises(ValueError):
		player.place_tree(tree2, row2, column2)

def test_shuffle_deck(deck):
	pre_shuffle_pickle = pickle.dumps(deck.cards)
	deck.shuffle_deck()
	post_shuffle_pickle = pickle.dumps(deck.cards)
	assert pre_shuffle_pickle != post_shuffle_pickle

def test_establish_scorer_simple_case(player, player2):
	player.trees_on_hand = ["Oak 2", "Oak 3", "Cassia 5", "Dogwood 6", "Dogwood 2", "Dogwood 3", "Jacaranda 5"]
	player2.trees_on_hand = ["Oak 8", "Cassia 8", "Dogwood 4", "Dogwood 5", "Jacaranda 7"]
	trees = ["Cassia", "Dogwood", "Jacaranda", "Oak"]
	scorer_dict = Scorer.calculate_scorer([player, player2], trees)
	assert scorer_dict["Cassia"] == [player2]
	assert scorer_dict["Dogwood"] == [player]
	assert scorer_dict["Jacaranda"] == [player2]
	assert scorer_dict["Oak"] == [player2]

def test_establish_scorer_both_score(player, player2):
	player.trees_on_hand = ["Oak 2", "Oak 3", "Cassia 5", "Cassia 2"]
	player2.trees_on_hand = ["Oak 5", "Cassia 7"]
	trees = ["Cassia", "Oak"]
	scorer_dict = Scorer.calculate_scorer([player, player2], trees)
	assert player1 in scorer_dict["Cassia"]
	assert player2 in scorer_dict["Cassia"]
	assert player1 in scorer_dict["Oak"]
	assert player2 in scorer_dict["Oak"]

def test_establish_scorer_no_one_scores(player, player2):
	player.trees_on_hand = ["Oak 1", "Oak 2", "Oak 3"]
	player2.trees_on_hand = []
	trees = ["Cassia", "Dogwood", "Jacaranda", "Lilac", "Magnolia", "Maple", "Olive"]
	scorer_dict = Scorer.calculate_scorer([player, player2], trees)
	assert scorer_dict["Cassia"] == None
	assert scorer_dict["Dogwood"] == None
	assert scorer_dict["Jacaranda"] == None
	assert scorer_dict["Lilac"] == None
	assert scorer_dict["Magnolia"] == None
	assert scorer_dict["Maple"] == None
	assert scorer_dict["Olive"] == None

def test_establish_scorer_8_vs_1(player, player2):
	player.trees_on_hand = ["Oak 1"]
	player2.trees_on_hand = ["Oak 8"]
	scorer_dict = Scorer.calculate_scorer([player, player2], trees)
	assert scorer_dict["Oak"] == player
