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

# What to implement next?
# > Basic points counting
# > Basic turn management 
# > Basic user input
# > Graveyard
# > Core loop --> Placing multiple cards on a board
# > Check for adjacency
# > 

# Use list comprehension to generate the full deck of cards

class Board():
	def __init__(self,rows:int=config.BOARD_ROWS, columns:int=config.BOARD_COLUMNS, empty_loc_symbol:str = "[   ]"):
		self.empty_loc_symbol = empty_loc_symbol
		# TODO - rename rows to row_amount and columns to columns_amount
		self.rows = rows
		self.columns = columns
		self.board_grid = self._create_empty_board_grid()
		

	def _create_empty_board_grid(self):
		new_board_grid = []
		for row in range(self.rows):
			new_board_grid.append(([self.empty_loc_symbol] * self.columns))
		return new_board_grid

	def print_board(self):
		for row in self.board_grid:
			print(" ".join(row))

	def _check_if_occupied_loc(self, row, column):
		if self.board_grid[row][column] == self.empty_loc_symbol:
			return False
		else:
			return True

	def check_if_valid_board_location(self, row, column):
		if row < 0 or column < 0:
			raise ValueError("Row and column locations need to be >= 0")
		if row > self.rows:
			raise ValueError("Provided row index is outside of board")
		if column > self.columns:
			raise ValueError("Provided column index is outside of board")
		if self.board_grid[row][column] != self.empty_loc_symbol:
			raise ValueError("Board space is occupied by another tree")

	def check_if_tree_has_adjacent_tree(self, row, column):
		has_adjacent_tree = False
		
		if column - 1 >= 0:
			if self._check_if_occupied_loc(row, column-1):
				has_adjacent_tree = True
		if column + 1 <= self.columns:
			if self._check_if_occupied_loc(row, column+1):
				has_adjacent_tree = True
		if row - 1 >= 0:
			if self._check_if_occupied_loc(row-1, column):
				has_adjacent_tree = True
		if row + 1 <= self.rows:
			if self._check_if_occupied_loc(row+1, column):
				has_adjacent_tree = True
		print(has_adjacent_tree)
		return has_adjacent_tree

		 
class Deck():
	def __init__(self):
		self.cards = ["Oak 1",
		"Oak 2",
		"Oak 3",
		"Oak 4",
		"Oak 5",
		"Oak 6",
		"Oak 7"]

	def remove_top_card(self):
		del self.cards[0]

	def shuffle_deck(self):
		raise NotImplemented()

class Player():
	def __init__(self, deck:Deck, board:Board):
		self.trees_on_hand = ["Oak 1", "Oak 2"]
		self.deck = deck
		self.board = board

	def place_tree(self, tree:str, row:int, column:int):
		if tree not in self.trees_on_hand:
			raise ValueError(f"You cannot play card {tree} you don't have in your hand: {self.trees_on_hand}")
		
		self.board.check_if_valid_board_location(row, column)

		# TODO - fix the below
		# TODO - implement to only check adjacency after first tree is placed
		# Start of logic to remove once there's a turn counter		
		temp_board_grid = self.board.board_grid.copy()
		temp_board_grid.count(self.board.empty_loc_symbol) == len(temp_board_grid)
		# for i in temp_board_grid:
		# 	i.remove(self.board.empty_loc_symbol)
		# if len(temp_board_grid) != 0:
		# 	print(temp_board_grid)
			# End of logic to remove once there's a turn counter		
			#print(self.board.check_if_tree_has_adjacent_tree(row, column))
			if not self.board.check_if_tree_has_adjacent_tree(row, column):
				raise ValueError(f"You cannot place a tree that's not adjacent to an existing tree")

		self.board.board_grid[row][column] = config.DECK_SHORTHANDS[tree]
		self.trees_on_hand.remove(tree)


	def draw_card(self):
		self.trees_on_hand.append(self.deck.cards[0])
		self.deck.remove_top_card()


if __name__ == "__main__":
	board = Board()
	deck = Deck()
	player = Player(deck, board)
	player.place_tree("Oak 1", row=4, column=5)
	player.place_tree("Oak 2", row=4, column=6)
	#player.draw_card()
	board.print_board()
