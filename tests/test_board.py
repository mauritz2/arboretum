from app import Card


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
