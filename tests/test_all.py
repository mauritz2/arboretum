import pytest
import pickle
from app import Board, Deck, Scorer, Player, config


@pytest.fixture
def board():
    return Board(num_rows=5, num_columns=2)


@pytest.fixture
def deck():
    return Deck()


@pytest.fixture
def player(board, deck):
    player = Player(name="Player 1", deck=deck, board=board)
    player.trees_on_hand = ["Oak 2", "Oak 3", "Oak 1", "Dogwood 6", "Dogwood 2", "Dogwood 3", "Jacaranda 5"]
    return player


@pytest.fixture
def player2(board, deck):
    return Player(name="Player 2", deck=deck, board=board)


@pytest.fixture
def scorer(player, player2):
    return Scorer(players=[player, player2], trees=["Cassia", "Dogwood", "Jacaranda", "Oak"])


def test_create_board_grid(board):
    assert (len(board.board_grid) == 5)


def test_place_tree(player):
    tree = "Oak 1"
    row, column = 0, 1
    player.place_tree(tree, row, column)
    assert player.board.board_grid[0][1] == config.CARD_SHORTHANDS[tree]


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
    card_to_draw = player.deck.cards[0]
    player.draw_card()
    assert card_to_draw in player.trees_on_hand


def test_remove_drawn_card_from_deck(player):
    card_to_draw = player.deck.cards[0]
    player.draw_card()
    assert card_to_draw not in player.deck.cards


def test_check_if_occupied_loc(board):
    row = 1
    column = 1
    check_occupied = board._check_if_occupied_loc(row, column)
    assert (check_occupied is False)
    board.board_grid[row][column] = "Oak 1"
    check_occupied = board._check_if_occupied_loc(row, column)
    assert (check_occupied is True)


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
    row2, column2 = 1, 1
    player.place_tree(tree1, row1, column1)
    with pytest.raises(ValueError):
        player.place_tree(tree2, row2, column2)


def test_shuffle_deck(deck):
    pre_shuffle_pickle = pickle.dumps(deck.cards)
    deck.shuffle_deck()
    post_shuffle_pickle = pickle.dumps(deck.cards)
    assert pre_shuffle_pickle != post_shuffle_pickle


def test_establish_scoring_players_simple_case(player, player2, scorer):
    player.trees_on_hand = ["Oak 2", "Oak 3", "Cassia 5", "Dogwood 6", "Dogwood 2", "Dogwood 3", "Jacaranda 5"]
    player2.trees_on_hand = ["Oak 8", "Cassia 8", "Dogwood 4", "Dogwood 5", "Jacaranda 7"]
    scorer.players = [player, player2]
    scorer_dict = scorer.calculate_scoring_players_by_tree()
    assert scorer_dict["Cassia"][0] is player2
    assert scorer_dict["Dogwood"][0] is player
    assert scorer_dict["Jacaranda"][0] is player2
    assert scorer_dict["Oak"][0] is player2


def test_establish_scorering_players_both_score(player, player2, scorer):
    player.trees_on_hand = ["Oak 2", "Oak 3", "Cassia 5", "Cassia 2"]
    player2.trees_on_hand = ["Oak 5", "Cassia 7"]
    scorer.players = [player, player2]
    scorer_dict = scorer.calculate_scoring_players_by_tree()
    assert player in scorer_dict["Cassia"]
    assert player2 in scorer_dict["Cassia"]
    assert player in scorer_dict["Oak"]
    assert player2 in scorer_dict["Oak"]


def test_establish_scoring_players_empty_hands(player, player2, scorer):
    player.trees_on_hand = []
    player2.trees_on_hand = []
    players = [player, player2]
    scorer.players = players
    scorer.trees = ["Cassia", "Dogwood", "Jacaranda", "Lilac", "Magnolia", "Maple", "Olive"]
    scorer_dict = scorer.calculate_scoring_players_by_tree()
    for p in players:
        assert p in scorer_dict["Cassia"]
        assert p in scorer_dict["Dogwood"]
        assert p in scorer_dict["Jacaranda"]
        assert p in scorer_dict["Lilac"]
        assert p in scorer_dict["Magnolia"]
        assert p in scorer_dict["Maple"]
        assert p in scorer_dict["Olive"]


def test_get_played_cards_by_type(player):
    player.trees_on_hand = ["Oak 2", "Oak 5", "Cassia 5", "Cassia 2"]
    oak_trees_played_expected = ["O2", "O5"]
    player.place_tree("Oak 2", 0, 0)
    player.place_tree("Oak 5", 0, 1)

    oak_trees_played = player.board.get_played_cards_of_type("Oak")

    # Order of what is returned doesn't matter
    oak_trees_played.sort()
    oak_trees_played_expected.sort()

    assert oak_trees_played == oak_trees_played_expected

def test_get_played_cards_by_type_empty_board(board):
	oak_trees_played = board.get_played_cards_of_type("Oak")
	assert oak_trees_played == []

    # def test_establish_scorering_players_8_vs_1(player, player2, scorer):
    # 	player.trees_on_hand = ["Oak 1"]
    # 	player2.trees_on_hand = ["Oak 8"]
    # 	scorer_dict = scorer.calculate_scoring_players_by_tree()
    # 	assert len(scorer_dict["Oak"]) == 1
    # 	assert scorer_dict["Oak"][0] is player
    #
    # def _test_find_straight_path(player, scorer):
    # 	player.trees_on_hand ["Oak 2", "Cassia 5", "Oak 7"]
    # 	player.place_tree(player.trees_on_hand[0], row=0, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=1, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=1, column=1)
    # 	scorer.players=[player]
    # 	paths = scorer.find_paths(tree_type="Oak")
    # 	assert paths[0] = ["O2", "C5", "O7"]
    #
    # def _test_find_path_endpoint_coordinates(player, scorer)
    # 	player.trees_on_hand ["Oak 2", "Oak 4" "Cassia 5", "Oak 6" "Oak 7"]
    # 	player.place_tree(player.trees_on_hand[0], row=0, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=1, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=2, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=3, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=4, column=0)
    #
    # 	scorer.players=[player]
    # 	coordinates = scorer.find_potential_path_endpoint_coordinates(tree_type="Oak")
    # 	assert coordinates == [[(0,0),(1,0)],
    # 	[(0,0),(3,0)],
    # 	[(0,0),(4,0)],
    # 	[(1,0),(3,0)],
    # 	[(1,0),(4,0)],
    # 	[(3,0),(4,0)],
    #
    #
    #
    # 	# Length
    # 	# 0 -1
    # 	# O1, O2, O3, O4, O6
    #
    #
    # def _test_find_curved_path(player):
    # 	pass
    #
    # def _test_find_multiple_paths(player):
    # 	pass
    #
    #

    # test_find_top_score
    # test_find_scoring_players
    # test_sum_cards
    # test_check_if_tree_on_hand
    # test_calculate_hand_sums
    #

    # def test_no_duplicates in deck()