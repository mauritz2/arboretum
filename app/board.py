import config
from typing import Literal


class Board:
    """
    Class to hold the board attributes, state (i.e. what cards have been placed) and validate card placement

    TODO - there should be methods to easily query the board - e.g. give all locations with a specific tree
    """

    def __init__(self, num_rows: int = config.BOARD_ROWS,
                 num_columns: int = config.BOARD_COLUMNS,
                 empty_loc_symbol: str = "[  ]"):
        self.empty_loc_symbol = empty_loc_symbol
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.board_grid = self._create_empty_board_grid()

    def _create_empty_board_grid(self):
        new_board_grid = []
        for row in range(self.num_rows):
            new_board_grid.append(([self.empty_loc_symbol] * self.num_columns))
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
        Checks if a location falls within the board boundaries and that it's empty
        """
        # TODO - refactor so row, column are a coordinates tuple (x, y)
        if row < 0 or column < 0:
            raise ValueError("Row and column locations need to be >= 0")
        if row > self.num_rows:
            raise ValueError("Provided row index is outside of board")
        if column > self.num_columns:
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
            if self._check_if_occupied_loc(row, column - 1):
                has_adjacent_tree = True
        if column + 1 < self.num_columns:
            if self._check_if_occupied_loc(row, column + 1):
                has_adjacent_tree = True
        if row - 1 >= 0:
            if self._check_if_occupied_loc(row - 1, column):
                has_adjacent_tree = True
        if row + 1 < self.num_rows:
            if self._check_if_occupied_loc(row + 1, column):
                has_adjacent_tree = True
        return has_adjacent_tree

    def get_played_cards_of_type(self, tree_type: Literal[config.TREES]) -> list[str]:
        """
        Returns a list of the cards played on the board,
        returns an empty list if no cards of the specified type were found
        """
        if tree_type not in config.TREES:
            raise ValueError("Trying to find cards for a tree type that doesn't exist")

        # TODO - it would be better if the board held the full card name (or tile class) and \
        # the the print board functionality turned it into shorthands - saves transformations back and forth
        tree_shorthand = config.CARD_SHORTHANDS_2[tree_type]

        cards_of_type_played = []
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                card = self.board_grid[i][j].item()
                if tree_shorthand in card:
                    cards_of_type_played.append(card)

        return cards_of_type_played
