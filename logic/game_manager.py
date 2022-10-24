from logic.scorer import Scorer
from enum import Enum


class GameManager:
    """
    Class to manage the phases of the game, i.e. who's turn it is,
    what phase in the current turn it is, when the game is over. The Game Manager also sets up the game,
    e.g. creating the scorer with the right amount of players.
    # TODO - rename to game_manager.py and Game_Manager class?
    # TODO - add the GameState manipulations into this class, as opposed to having the web app do we logic
    # TODO - create dummy funcs for the things arboretum.py reference the game_manager for. Make everything else _
    """

    def __init__(self, scorer: Scorer) -> None:
        self.scorer = scorer
        #self.current_player_index = 0
        self.has_not_taken_turn = self.scorer.players
        #self.current_player = self.scorer.players[self.current_player_index]
        self.current_player = self._get_next_player()
        self.game_phase = GameState.CHOOSE_WHAT_TO_DRAW
        self.num_cards_drawn_current_turn = 0
        self.selected_card_to_play = None

    def start_next_round(self):
        """
        Checks if the game is over - if not switch to the next player so they can take their turn
        """

        self.game_phase = GameState.CHOOSE_WHAT_TO_DRAW
        self.num_cards_drawn_current_turn = 0
        self.selected_card_to_play = None
        self.current_player_index = self._get_next_player_index()
        print(f"\nThe next player will be {self.current_player_index}\n")
        self.current_player = self.scorer.players[self.current_player_index]

    def check_if_game_is_over(self):
        """
        Returns true if the game is over (i.e. deck is empty). Otherwise returns false.
        """
        if self.scorer.players[0].deck.get_amt_of_cards_left() <= 0:
            return True
        else:
            return False

    def _get_next_player(self):
        """
        Returns the next player instance to take its turn. All players take one turn in a pre-determined order,
        and then it goes back to the first player
        """
        if len(self.has_not_taken_turn) == 0:
            # Everybody has taken their turn - resetting to new round
            self.has_not_taken_turn = self.scorer.players
        return self.has_not_taken_turn.pop()


    # def _get_next_player_index(self):
    #     """
    #     Gets the next index for the next player
    #     or return 0 to start over from the first player if the last player just took their turn
    #     """
    #     i = self.current_player_index
    #     print(f"The current index is {i}")
    #     print(f"Value to be compared against {len(self.scorer.players)}")
    #     i += 1
    #     if i >= len(self.scorer.players):
    #         i = 0
    #     print(f"The new i is {i}")
    #     return i

    def get_winner(self):
        winners, top_paths = self.scorer.determine_winner()
        return winners, top_paths


class GameState(Enum):
    # TODO - turn into str enum - easier to work with (have to upgrade Python to the latest version)
    CHOOSE_WHAT_TO_DRAW = "Draw"
    CHOOSE_CARD_TO_PLAY = "Choose Card"
    CHOOSE_WHERE_TO_PLAY = "Choose Coords"
    CHOOSE_DISCARD = "Choose Discard"
    SCORING = "Scoring"


player_game_state_messages = {
    GameState.CHOOSE_WHAT_TO_DRAW: "Draw two cards from either the deck or one of the discard piles",
    GameState.CHOOSE_CARD_TO_PLAY: "Select a card to play",
    GameState.CHOOSE_WHERE_TO_PLAY: "Select a location on the board where you want to place your card",
    GameState.CHOOSE_DISCARD: "Choose a card to discard. It will appear in your discard pile.",
    GameState.SCORING: "The game is over"
}