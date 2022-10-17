from logic import Card
import pytest

def test_shape_create_empty_board_grid(board):
    assert (len(board.board_grid) == 10) and (len(board.board_grid[0]) == 10)


def test_tiles_create_empty_board_grid(board):
    assert isinstance(board.board_grid[0][0], Card)

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
    board.board_grid[5][1] = Card(tree_type="Blue Spruce", tree_val=8)

    oak_trees_played = board.get_played_cards_of_type("Oak")

    assert oak_trees_played == oak_trees_played_expected


def test_find_adjacent_incrementing_cards(board):

    oak4 = Card(tree_type="Oak", tree_val=4)
    oak1 = Card(tree_type="Oak", tree_val=1)
    jac6 = Card(tree_type="Jacaranda", tree_val=6)
    blue1 = Card(tree_type="Blue Spruce", tree_val=1)
    blue7 = Card(tree_type="Blue Spruce", tree_val=7)
    blue8 = Card(tree_type="Blue Spruce", tree_val=8)

    # Target location
    board.board_grid[2][2] = Card(tree_type="Jacaranda", tree_val=5)

    # Adjacent and incrementing
    board.board_grid[2][3] = blue7
    board.board_grid[3][2] = blue8

    # Adjacent but non-incrementing
    board.board_grid[1][2] = oak1
    board.board_grid[2][1] = oak4

    # Non-adjacent
    board.board_grid[5][5] = oak1
    board.board_grid[0][0] = blue1
    board.board_grid[1][1] = oak4
    board.board_grid[3][3] = jac6

    incremental_adjacent = board.get_adjacent_cards(row=2, column=2, ignore_tree_val=False)
    incremental_adj_expected = [blue7, blue8]

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
    board.board_grid[5][5] = Card(tree_type="Blue Spruce", tree_val=7)

    incremental_adjacent = board.get_adjacent_cards(row=2, column=2, ignore_tree_val=False)
    assert len(incremental_adjacent) == 0


def test_find_adjacent_incrementing_cards_out_of_bounds_check(board):
    """
    Make sure code handles case when cards are next to the board edge
    """
    board.board_grid[5][0] = Card(tree_type="Jacaranda", tree_val=5)
    board.board_grid[4][0] = Card(tree_type="Jacaranda", tree_val=6)
    board.board_grid[0][9] = Card(tree_type="Oak", tree_val=4)
    board.board_grid[0][8] = Card(tree_type="Blue Spruce", tree_val=7)

    incremental_adjacent = board.get_adjacent_cards(row=5, column=0, ignore_tree_val=False)
    assert incremental_adjacent == [Card(tree_type="Jacaranda", tree_val=6)]
    incremental_adjacent = board.get_adjacent_cards(row=0, column=9, ignore_tree_val=False)
    assert incremental_adjacent == [Card(tree_type="Blue Spruce", tree_val=7)]

def test_find_adjacent_incrementing_cards_no_card(board):
    """
    When we specify a location without a card we expect an error since there's nothing to assess
    if incremental without a card at the specified location
    """
    with pytest.raises(ValueError):
        board.get_adjacent_cards(row=2, column=2, ignore_tree_val=False)


def test_find_coords_of_card(board):
    jac5 = Card(tree_type="Jacaranda", tree_val=5)
    board.board_grid[2][3] = jac5
    coords = board.find_coords_of_card(jac5)
    assert coords == (2, 3)


def test_find_coords_of_card_not_played(board):
    jac5 = Card(tree_type="Jacaranda", tree_val=5)
    coords = board.find_coords_of_card(jac5)
    assert coords is None