import pytest
from arboretum.game.logic.card import Card
from conftest import cards as c


def test_shape_create_empty_board_grid(board):
    """
    Verify board setup dimensions
    """
    assert (len(board.board_grid) == 10) and (len(board.board_grid[0]) == 10)


def test_tiles_create_empty_board_grid(board):
    """
    Verify that empty board is set up with Card instances
    """
    assert isinstance(board.board_grid[0][0], Card)


def test_get_played_cards_by_type_empty_board(board):
    """
    Verify that board returns empty list if no c of type have been played
    """
    oak_trees_played = board.get_played_cards_of_type("Oak")
    assert oak_trees_played == []


def test_get_played_cards_by_type(board):
    """
    Verify that board can return all played cards of a specific type
    """
    oak_trees_played_expected = [c["Oak 2"], c["Oak 3"], c["Oak 8"]]

    board.board_grid[2][2] = c["Oak 2"]
    board.board_grid[3][2] = c["Oak 3"]
    board.board_grid[4][2] = c["Oak 8"]
    board.board_grid[5][3] = c["Jacaranda 8"]
    board.board_grid[5][1] = c["Blue Spruce 8"]

    oak_trees_played = board.get_played_cards_of_type("Oak")

    assert oak_trees_played == oak_trees_played_expected


def test_find_adjacent_incrementing_cards(board):
    """
    Verify that board can return all adjacent cards with a higher value to a given card
    """
    # Target location
    board.board_grid[2][2] = c["Jacaranda 5"]

    # Adjacent and incrementing
    board.board_grid[2][3] = c["Blue Spruce 7"]
    board.board_grid[3][2] = c["Blue Spruce 8"]

    # Adjacent but non-incrementing
    board.board_grid[1][2] = c["Oak 1"]
    board.board_grid[2][1] = c["Oak 4"]

    # Non-adjacent
    board.board_grid[5][5] = c["Oak 1"]
    board.board_grid[0][0] = c["Blue Spruce 1"]
    board.board_grid[1][1] = c["Oak 4"]
    board.board_grid[3][3] = c["Jacaranda 6"]

    incremental_adjacent = board.get_adjacent_cards(row=2, column=2, ignore_tree_num=False)
    incremental_adj_expected = [c["Blue Spruce 7"], c["Blue Spruce 8"]]

    incremental_adjacent.sort()
    incremental_adj_expected.sort()

    assert incremental_adjacent == incremental_adj_expected


def test_find_adjacent_incrementing_cards_no_adjacencies(board):
    """
    When there are no adjacencies we expect an empty list back
    """
    board.board_grid[2][2] = c["Jacaranda 5"]
    board.board_grid[0][0] = c["Oak 4"]
    board.board_grid[4][4] = c["Jacaranda 6"]
    board.board_grid[5][5] = c["Blue Spruce 7"]

    incremental_adjacent = board.get_adjacent_cards(row=2, column=2, ignore_tree_num=False)
    assert len(incremental_adjacent) == 0


def test_find_adjacent_incrementing_cards_out_of_bounds_check(board):
    """
    Verify that code doesn't throw index out of range when cards are next to the board edge
    """
    board.board_grid[5][0] = c["Jacaranda 5"]
    board.board_grid[4][0] = c["Jacaranda 6"]
    board.board_grid[0][9] = c["Oak 4"]
    board.board_grid[0][8] = c["Blue Spruce 7"]

    incremental_adjacent = board.get_adjacent_cards(row=5, column=0, ignore_tree_num=False)
    assert incremental_adjacent == [c["Jacaranda 6"]]
    incremental_adjacent = board.get_adjacent_cards(row=0, column=9, ignore_tree_num=False)
    assert incremental_adjacent == [c["Blue Spruce 7"]]


def test_find_adjacent_incrementing_cards_no_card(board):
    """
    When ask to find adjacent cards with a higher value, but we specify an empty board
    location as the center card we expect an error
    """
    with pytest.raises(ValueError):
        board.get_adjacent_cards(row=2, column=2, ignore_tree_num=False)


def test_find_coords_of_card(board):
    """
    Verify that we can find the board coordinates of a card
    """
    board.board_grid[2][3] = c["Jacaranda 5"]
    coords = board.find_coords_of_card(c["Jacaranda 5"])
    assert coords == (2, 3)


def test_find_coords_of_card_not_played(board):
    """
    Verify we get None if the card we asked for doesn't exist on the board
    """
    coords = board.find_coords_of_card(c["Jacaranda 5"])
    assert coords is None


def test_get_board_state(board):
    """
    Verify we get None if the card we asked for doesn't exist on the board
    """
    board.board_grid[0][0] = Card(tree_type="Oak", tree_num=5)
    board.board_grid[9][9] = Card(tree_type="Cassia", tree_num=8)
    board_state = board.get_board_state()
    expected_board_state = [["Oak 5", None, None, None, None, None, None, None, None, None]] + [[None, None, None, None, None, None, None, None, None, None]] * 8 + [[None, None, None, None, None, None, None, None, None, "Cassia 8"]]
    assert board_state == expected_board_state
