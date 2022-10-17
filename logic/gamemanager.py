from logic.player import Player
from logic.discard import Discard
from logic.deck import Deck
from logic.board import Board
from logic.scorer import Scorer
from enum import Enum
import logic.config as config


class GameManager:
    """
    Class to manage the phases of the game, i.e. who's turn it is,
    what phase in the current turn it is, when the game is over. The Game Manager also sets up the game,
    e.g. creating the scorer with the right amount of players.
    """

    def __init__(self, num_players: int) -> None:
        self.num_players = num_players
        self.scorer = self.setup_scorer()
        self.game_over = False
        self.current_player_index = 0
        self.current_player = self.scorer.players[self.current_player_index]
        self.game_phase = GameState.CHOOSE_WHAT_TO_DRAW
        self.num_cards_drawn_current_turn = 0
        self.selected_card_to_play = None

    def setup_scorer(self) -> Scorer:
        """
        Creates all the class instances needed to run the game, including the Scorer
        which contains all the players and their respective boards, decks, discard piles
        Returns a Scorer instance which contain all the instances to run the game
        """

        players = []
        deck = Deck()
        for i in range(self.num_players):
            player_name = f"Player {i + 1}"
            discard = Discard(cards=[])
            board = Board(num_rows=config.BOARD_ROWS, num_columns=config.BOARD_COLUMNS)

            player = Player(name=player_name,
                            deck=deck,
                            discard=discard,
                            board=board
                            )
            players.append(player)

        scorer = Scorer(players=players)
        return scorer

    def start_next_round(self):
        """
        Checks if the game is over - if not switch to the next player so they can take their turn
        """

        self.game_phase = GameState.CHOOSE_WHAT_TO_DRAW
        self.num_cards_drawn_current_turn = 0
        self.selected_card_to_play = None
        self.current_player_index = self._get_next_player_index()
        self.current_player = self.scorer.players[self.current_player_index]

    def check_if_game_is_over(self):
        """
        Returns true if the game is over (i.e. deck is empty). Otherwise returns false.
        """
        if self.scorer.players[0].deck.get_amt_of_cards_left() <= 0:
            return True
        else:
            return False

    def _get_next_player_index(self):
        """
        Gets the next index for the next player
        or return 0 to start over from the first player if the last player just took their turn
        """
        i = self.current_player_index
        i += 1
        if i >= len(self.scorer.players):
            i = 0
        return i

    def get_winner(self):
        winners, top_paths = self.scorer.determine_winner()
        return winners, top_paths


class GameState(Enum):
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