import config
import random

# Rules reminder
# > 8 cards, 8 colors - 64 cards in a deck of 4 players. Only 4 colors for 2 players.
# Turn order
# > Draw 2 cards (your deck, discard piles)
# > Play 1 card
# > Discard 1 card
# Points
# > 1 point for each card in the path
# > At least 4 cards in the same color? Then 1 additional point
# > 1 additional point if paths begins with a 1
# > 2 additional points if you end with an 8

# TBD
# > Should user be allowed to place the first one anywhere? Or just dead center every time?
# > Should each card be a tuple with a string and an int maybe? For easier summing

# What to implement next?
# > Basic points counting
# > Determining what player "scores" for each tree
# > Basic turn management 
# > Basic user input
# > Graveyard and drawing from graveyard

class Board():
	def __init__(self,rows:int=config.BOARD_ROWS, columns:int=config.BOARD_COLUMNS, empty_loc_symbol:str = "[  ]"):
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
		"""
		Checks if a location on the board already has a card placed there or not
		"""
		if self.board_grid[row][column] == self.empty_loc_symbol:
			return False
		else:
			return True

	def check_if_valid_board_location(self, row, column):
		"""
		Checks if a location falls within the board boundries and that it's empty
		"""
		if row < 0 or column < 0:
			raise ValueError("Row and column locations need to be >= 0")
		if row > self.rows:
			raise ValueError("Provided row index is outside of board")
		if column > self.columns:
			raise ValueError("Provided column index is outside of board")
		if self.board_grid[row][column] != self.empty_loc_symbol:
			raise ValueError("Board space is occupied by another tree")

	def check_if_tree_has_adjacent_tree(self, row, column):
		"""
		Checks if a specific location on the board has an adjacently placed tree
		"""
		has_adjacent_tree = False
		
		if column - 1 >= 0:
			if self._check_if_occupied_loc(row, column-1):
				has_adjacent_tree = True
		if column + 1 < self.columns:
			if self._check_if_occupied_loc(row, column+1):
				has_adjacent_tree = True
		if row - 1 >= 0:
			if self._check_if_occupied_loc(row-1, column):
				has_adjacent_tree = True
		if row + 1 < self.rows:
			if self._check_if_occupied_loc(row+1, column):
				has_adjacent_tree = True
		return has_adjacent_tree

		 
class Deck():
	def __init__(self, tree_types:list=config.TREES, num_cards_per_type:int=config.CARDS_PER_TREE_TYPE):
		self.cards = self._generate_deck(tree_types, num_cards_per_type)

		self.shuffle_deck()

	def _generate_deck(self, tree_types, num_cards_per_type):
		cards = []
		for tree in tree_types:
			for i in range(num_cards_per_type):
				card_name = f"{tree} {i+1}"
				cards.append(card_name)
		return cards

	def remove_top_card(self):
		del self.cards[0]

	def shuffle_deck(self):
		random.shuffle(self.cards)

class Player():
	def __init__(self, deck:Deck, board:Board, num_cards_starting_hand:int=config.NUM_CARDS_STARTING_HAND):
		self.trees_on_hand = []
		self.deck = deck
		self.board = board
		self.first_tree_placed = False

		for i in range(num_cards_starting_hand):
			self.draw_card()

	def place_tree(self, tree:str, row:int, column:int):
		if tree not in self.trees_on_hand:
			raise ValueError(f"You cannot play card {tree} you don't have in your hand: {self.trees_on_hand}")
		
		self.board.check_if_valid_board_location(row, column)

		if self.first_tree_placed:
			if not self.board.check_if_tree_has_adjacent_tree(row, column):
					raise ValueError(f"You cannot place a tree that's not adjacent to an existing tree")

		self.board.board_grid[row][column] = config.DECK_SHORTHANDS[tree]
		self.trees_on_hand.remove(tree)
		self.first_tree_placed = True


	def draw_card(self):
		# TODO - implement drawing from Graveyard
		self.trees_on_hand.append(self.deck.cards[0])
		self.deck.remove_top_card()

	def discard_card(self):
		raise NotImplemented()

class Scorer():
	def __init__(self, players:list, trees:list=config.TREES):
		self.players = players
		self.trees = trees

	def establish_scorer(self):
		for player in self.players:
			player_sum_by_tree = {}
			hand = player.trees_on_hand
			for tree in self.trees:
				matching_cards = [card for card in hand if tree in card]
				total_sum = self._sum_cards(matching_cards)
				player_sum_by_tree[tree] = total_sum
		# TODO - continue here



	def _sum_cards(self, cards):
		total = 0
		for card in cards:
			total += int(card[-1])
		return total


	def find_paths():
		pass 
		# TODO 
		# Cycle through the tree types
		# For each type run tests
			# Do you have a at least two cards of this type?
				 # If yes - run logic below
				 # If no - put this tree's path to 0
			# From the lowest denominator card (i.e. start) - check adjacents
				# Loop through each adjacent
					# Track the current num of the card for the current candidate path, refresh on finding new valid adjacent
					# Is it the end tree and it's ascending from current position? If so complete a path and score
					# Is it not ascending? If so ignore
					# Is it ascending? If so go to that node and re-run loop
		# Maybe the best way to do this is through recursion lol
		# Note that there can be more than 1 valid path - need to find the top scorer
		# This should return a dict of all valid paths and an int for the score

if __name__ == "__main__":
	board = Board()
	deck = Deck()
	player = Player(deck, board)
	player.place_tree(player.trees_on_hand[0], row=4, column=5)
	player.place_tree(player.trees_on_hand[0], row=4, column=6)
	print(f"Player hand is {player.trees_on_hand}")
	#player.board.print_board()
	scorer = Scorer([player, player2])
	scorer.establish_scorer()

