import config

class Board():
	"""
	Class to hold the board attributes, state (i.e. what cards have been placed) and validate card placement
	"""
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
		# TODO - refactor so row, column are a coordinates tuple (x, y)
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
		# TODO - Refactor to define dirs = [(-1,0), (1,0), (0,1), (0,-1)]
		# and then for x, y in dirs + a check if it's out of bounds to do nothing
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
