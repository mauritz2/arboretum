from app import Card
import pytest

def test_shape_create_empty_board_grid(board):
    assert (len(board.board_grid) == 10) and (len(board.board_grid[0]) == 10)


def test_tiles_create_empty_board_grid(board):
    assert isinstance(board.board_grid[0][0], Card)


def test_check_if_occupied_loc(board):
    row = 1
    column = 1
    check_occupied = board._check_if_occupied_loc(row, column)
    assert (check_occupied is False)
    board.board_grid[row][column] = Card(tree_type="Oak", tree_val=2)
    check_occupied = board._check_if_occupied_loc(row, column)
    assert (check_occupied is True)


def test_get_played_cards_by_type_empty_board(board):
	oak_trees_played = board.get_played_cards_of_type("Oak")
	assert oak_trees_played == []


def test_get_played_cards_by_type(board):
    oak_2 = Card(tree_type="Oak", tree_val=2)
    oak_3 = Card(tree_type="Oak", tree_val=3)
    oak_8 = Card(tree_type="Oak", tree_val=8)
    oak_trees_played_expected = [oak_2, oak_3, oak_8]

    board.board_grid[2][2] = oak_2
    board.board_grid[3][2] = oak_3
    board.board_grid[4][2] = oak_8
    board.board_grid[5][3] = Card(tree_type="Jacaranda", tree_val=8)
    board.board_grid[5][1] = Card(tree_type="Dogwood", tree_val=8)

    oak_trees_played = board.get_played_cards_of_type("Oak")

    assert oak_trees_played == oak_trees_played_expected


def test_find_adjacent_incrementing_cards(board):

    oak4 = Card(tree_type="Oak", tree_val=4)
    oak1 = Card(tree_type="Oak", tree_val=1)
    jac6 = Card(tree_type="Jacaranda", tree_val=6)
    dog1 = Card(tree_type="Dogwood", tree_val=1)
    dog7 = Card(tree_type="Dogwood", tree_val=7)
    dog8 = Card(tree_type="Dogwood", tree_val=8)

    # Target location
    board.board_grid[2][2] = Card(tree_type="Jacaranda", tree_val=5)

    # Adjacent and incrementing
    board.board_grid[2][3] = dog7
    board.board_grid[3][2] = dog8

    # Adjacent but non-incrementing
    board.board_grid[1][2] = oak1
    board.board_grid[2][1] = oak4

    # Non-adjacent
    board.board_grid[5][5] = oak1
    board.board_grid[0][0] = dog1
    board.board_grid[1][1] = oak4
    board.board_grid[3][3] = jac6

    incremental_adjacent = board.find_adjacent_incrementing_cards(row=2, column=2)
    incremental_adj_expected = [dog7, dog8]

    incremental_adjacent.sort()
    incremental_adj_expected.sort()

    assert incremental_adjacent == incremental_adj_expected


def test_find_adjacent_incrementing_cards_no_adjacencies(board):
    """
    When there are no adjacencies we expect an empty list back
    """
    board.board_grid[2][2] = Card(tree_type="Jacaranda", tree_val=5)
    board.board_grid[0][0] = Card(tree_type="Oak", tree_val=4)
    board.board_grid[4][4] = Card(tree_type="Jacaranda", tree_val=6)
    board.board_grid[5][5] = Card(tree_type="Dogwood", tree_val=7)

    incremental_adjacent = board.find_adjacent_incrementing_cards(row=2, column=2)
    assert len(incremental_adjacent) == 0


def test_find_adjacent_incrementing_cards_no_card(board):
    """
    When we specify a location without a card we expect an error since there's nothing to assess
    if incremental without a card at the specified location
    """
    with pytest.raises(ValueError):
        board.find_adjacent_incrementing_cards(row=2, column=2)


def test_get_possible_start_end_loc_pairs(scorer):
    oak1 = Card(tree_type="Oak", tree_val=1)
    oak2 = Card(tree_type="Oak", tree_val=2)
    oak4 = Card(tree_type="Oak", tree_val=4)
    oak8 = Card(tree_type="Oak", tree_val=8)

    cards = [oak1, oak2, oak4, oak8]

    expected_combos = [
        (oak1, oak2),
        (oak1, oak4),
        (oak1, oak8),
        (oak2, oak4),
        (oak2, oak8),
        (oak4, oak8),
    ]
    start_end_combos = scorer.get_possible_start_end_card_pairs(cards)

    start_end_combos.sort()
    expected_combos.sort()

    assert start_end_combos == expected_combos


def test_get_possible_start_end_loc_pairs_empty(scorer):
    assert scorer.get_possible_start_end_card_pairs([]) == []
