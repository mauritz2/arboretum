import logic.config as config
from typing import Literal
from logic.card import Card


class Board:
    """
    Class to hold the board attributes, state (i.e. what cards have been placed) and methods to validate card placement
    """

    def __init__(self, num_rows: int = config.BOARD_ROWS, num_columns: int = config.BOARD_COLUMNS):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.board_grid = self._create_empty_board_grid()

    def _create_empty_board_grid(self) -> list[list[Card]]:
        """
        Sets up an empty board which consists of empty lists.
        Board locations are referenced as [row][column]
        """
        empty_tile = Card(tree_type=None, tree_num=None)
        empty_board_grid = [([empty_tile] * self.num_columns) for i in range(self.num_rows)]
        return empty_board_grid

    def is_valid_board_location(self, row: int, column: int, check_if_occupied=True) -> (bool, str):
        """
        Checks if a location falls within the board boundaries. Can also check that it's empty (optional).
        Returns True if valid board location, False otherwise.
        """
        is_valid_board_loc = True
        error_msg = ""

        if row < 0 or column < 0:
            is_valid_board_loc = False
            error_msg = "Row and column locations need to be >= 0"
        if row >= self.num_rows:
            is_valid_board_loc = False
            error_msg = f"Provided row index {row} is outside of board max {self.num_rows}"
        if column >= self.num_columns:
            is_valid_board_loc = False
            error_msg = f"Provided column index {column} is outside of board max {self.num_columns}"
        if check_if_occupied:
            if self.board_grid[row][column].tree_type is not None:
                is_valid_board_loc = False
                error_msg = f"Board space at ({row},{column}) is already occupied by " \
                            f"{self.board_grid[row][column].name}"

        return is_valid_board_loc, error_msg

    def get_adjacent_cards(self, row: int, column: int, ignore_tree_num=True) -> list[Card]:
        """
        Returns all cards adjacent to a specified location on the board.
        Returns all adjacencies by default, but can be set to return incremental (i.e. only cards with a higher
        tree values than the specified card). Returns a ValueError if tree values are considered, but the provided
        location on the board is empty (i.e. there's no value to compare adjacent tree values to).
        """
        confirmed_adjacencies = []

        if not ignore_tree_num:
            center_tree_num = self.board_grid[row][column].tree_num
            if center_tree_num is None:
                raise ValueError(f"Can't find incrementing adjacent cards since location at ({row},{column}) is empty")

        coords_to_check = [(row - 1, column), (row + 1, column), (row, column + 1), (row, column - 1)]

        for coords in coords_to_check:
            is_valid_board_loc, _ = self.is_valid_board_location(coords[0], coords[1], check_if_occupied=False)
            if not is_valid_board_loc:
                continue

            potential_adjacency = self.board_grid[coords[0]][coords[1]]

            # tree_type = None indicates it's a blank slot on the board - i.e. not an adjacent card
            if potential_adjacency.tree_type is None:
                continue

            if not ignore_tree_num:
                # The adjacent tree has an equal or lower value to the center card - i.e. not a valid path
                if potential_adjacency.tree_num <= center_tree_num:
                    continue

            confirmed_adjacencies.append(potential_adjacency)

        return confirmed_adjacencies

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

    def find_coords_of_card(self, card: Card) -> (int, int):
        """
        Searches the board for a specific card and returns its row and column coordinates
        Returns None if the Card isn't found
        I think the comparison "if value is card" works here because since Card is a dataclass
        it automatically implements eq() - maybe ?
        """
        for row_coord, row in enumerate(self.board_grid):
            for col_coord, value in enumerate(row):
                if value is card:
                    return row_coord, col_coord
        else:
            return None

    def get_board_state(self):
        """
        Returns nested lists representing the board - with only the card names. I.e. no Card instances are returned.
        This is useful because the Card instance isn't serializable meaning it can't be sent to the front-end. The front-end
        also only needs the names so good for information hiding.
        """

        card_names_board = []
        for row in self.board_grid:
            card_names_row = []
            for card in row:
                card_names_row.append(card.name)
            card_names_board.append(card_names_row)

        return card_names_board
