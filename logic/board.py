import logic.config as config
from typing import Literal
from logic.card import Card


class Board:
    """
    Class to hold the board attributes, state (i.e. what cards have been placed) and methods to validate card placement
    """

    def __init__(self, num_rows: int = config.BOARD_ROWS,
                 num_columns: int = config.BOARD_COLUMNS,
                 empty_loc_symbol: str = "[  ]"):
        self.empty_loc_symbol = empty_loc_symbol
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.board_grid = self._create_empty_board_grid()

    def _create_empty_board_grid(self):
        empty_tile = Card(tree_type=None, tree_val=None)
        empty_board_grid = [([empty_tile] * self.num_columns) for i in range(self.num_rows)]
        return empty_board_grid

    def print_board(self):
        """
        Creates the visual representation of the board
        (i.e. using the visual shorthands for each card) and prints the result
        """
        # Create the visual representation of the board
        board_to_display = []
        # TODO - could be more efficient with list comprehension + getattr, but would need to deal with nested list
        for row in self.board_grid:
            display_row = []
            for value in row:
                display_shorthand = value.visual_shorthand
                display_shorthand = config.EMPTY_SLOT_DISPLAY_SHORTHAND if display_shorthand is None else display_shorthand
                display_row.append(display_shorthand)
            board_to_display.append(display_row)

        # Print the board
        for row in board_to_display:
            print(config.BOARD_SLOT_DIVIDER.join(row))

    def _check_if_occupied_loc(self, row, column):
        """
        Checks if a location on the board already has a card placed there or not
        Returns True if occupied, otherwise False
        """
        if self.board_grid[row][column].tree_type is not None:
            return True
        else:
            return False

    def check_if_valid_board_location(self, row, column):
        """
        Checks if a location falls within the board boundaries and that it's empty
        """
        # TODO - refactor so row, column are a coordinates tuple (x, y)
        if row < 0 or column < 0:
            raise ValueError("Row and column locations need to be >= 0")
        if row > self.num_rows:
            raise ValueError(f"Provided row index {row} is outside of board max {self.num_rows}")
        if column > self.num_columns:
            raise ValueError(f"Provided column index {column} is outside of board max {self.num_columns}")
        if self._check_if_occupied_loc(row, column):
            raise ValueError(f"Board space at ({row},{column}) is already occupied by {self.board_grid[row][column].card_name}")

    def check_if_slot_has_adjacent_tree(self, row, column):
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
            raise ValueError(f"Trying to find cards for a tree type {tree_type} that doesn't exist")

        cards_of_type_played = []
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                played_card = self.board_grid[i][j]
                if played_card.tree_type == tree_type:
                    cards_of_type_played.append(played_card)

        return cards_of_type_played

    def find_adj_increment_cards(self, row: int, column: int) -> list[Card]:
        """
        Given a location on the board, return a list of all adjacent played cards
        with a higher value than the card at the given location. Returns an error if the specified loc is empty
        This is used to find paths that consist of adjacent incrementing cards
        """
        center_tree_value = self.board_grid[row][column].tree_val

        if center_tree_value is None:
            raise ValueError(f"Can't find incrementing adjacent cards since location at ({row},{column}) is empty")

        incrementing_adjacent = []
        coords_to_check = [(row-1, column),
                         (row+1, column),
                         (row, column+1),
                         (row, column-1)]
        for coords in coords_to_check:
            # Check that the index isn't out of range which would cause an error
            if (coords[0] >= config.BOARD_ROWS) or (coords[1] >= config.BOARD_COLUMNS):
                continue
            if (coords[0] < 0) or (coords[1] < 0):
                continue

            card_at_loc = self.board_grid[coords[0]][coords[1]]

            if card_at_loc.tree_type is None:
                continue
            if card_at_loc.tree_val <= center_tree_value:
                # Adjacent tree doesn't have a higher val than center card, i.e. no valid path this way
                continue

            # The current coord location contains a tree that has a higher value than the center value
            # (i.e. indicating a possible path)
            incrementing_adjacent.append(card_at_loc)

        return incrementing_adjacent

    def find_coords_of_card(self, card:Card):
        """
        Searches the board for a specific card and returns its' row and column coordinates
        Returns None if the Card isn't found
        I think the comparison "if value is card" works here because since Card is a dataclass
        it automatically implements eq() - maybe ?
        # TODO - maybe rename row_coords and column_coord to x and y across the logic
        """
        # TODO - this type of nested for loop search is pretty common across the code - possible to vectorize?
        for row_coord, row in enumerate(self.board_grid):
            for col_coord, value in enumerate(row):
                if value is card:
                    return (row_coord, col_coord)
        else:
            return None
