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
			new_board_grid.append((["[   ]"] * columns))
		return new_board_grid


	def print_board(self):
		for row in self.board_grid:
			print(" ".join(row))

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

	def place_tree(self, tree:str, location:tuple):
		if tree not in self.trees_on_hand:
			raise ValueError(f"You cannot play card {tree} you don't have in your hand: {self.trees_on_hand}")
		
		self.trees_on_hand.remove(tree)
		self.board.board_grid[location[0]][location[1]] = config.DECK_SHORTHANDS[tree]

	def draw_card(self):
		self.trees_on_hand.append(self.deck.cards[0])
		self.deck.remove_top_card()





if __name__ == "__main__":
	board = Board()
	deck = Deck()
	player = Player(deck, board)
	player.place_tree("Oak 1", (2,3))
	player.draw_card()
	board.print_board()
