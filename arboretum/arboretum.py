import config

# 8 cards, 8 colors - 64 cards in a deck

# Turn order
# > Draw 2 cards (your deck, discard piles)
# > Play 1 card
# > Discard 1 card

# Should you allow the user to place the first one anywhere? Or just dead center every time?
# 

# Trees (8)
# Cassia, Dogwood, Jacaranda, Olive, Lilac, Magnolia, Maple, Oak

# Points
# 1 point for each card in the path
# At least 4 cards in the same color? Then 1 additional point
# 1 additional point if paths begins with a 1
# 2 additional points if you end with an 8

class Board():
	def __init__(self,rows=config.BOARD_ROWS, columns=config.BOARD_COLUMNS):
		self.board_grid = self._create_empty_board_grid(rows, columns)
		
	def _create_empty_board_grid(self,rows, columns):
		new_board_grid = []
		for row in range(rows):
			new_board_grid.append((["[  ]"] * columns))
		return new_board_grid


	def print_board(self):
		for row in self.board_grid:
			print(" ".join(row))


class Player():
	def __init__(self):
		self.cards_on_hand = []

	def place_tree(self, board:Board, location:tuple):
		# TODO - should remove card from ahnd and call method on board to place on board - PLayer shouldn't know that implementation 
		#print(len(board.board_grid[location[0]]))
		board.board_grid[location[0]][location[1]] = "[X]"


if __name__ == "__main__":
	board = Board()
	#board.print_board()
	player = Player()
	player.place_tree(board, (2,3))
	board.print_board()
