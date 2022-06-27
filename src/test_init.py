import arboretum


def test_create_empty_board_grid():
	board = Board(5, 2)
	assert(len(board) == 5)


