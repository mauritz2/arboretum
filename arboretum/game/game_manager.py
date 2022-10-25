from arboretum.game.logic.player import Player
from arboretum.game.logic.scorer import Scorer
from enum import Enum


class GameManager:
    """
    Class to manage the phases of the game, i.e. who's turn it is,
    what phase in the current turn it is, when the game is over. The Game Manager also sets up the game,
    e.g. creating the scorer with the right amount of players.

    This is the only game logic class that the Flask app app.py should reference. It hides the other
    functions and properties of the other classes

    # TODO - rename to game_manager.py and Game_Manager class?
    # TODO - add the GameState manipulations into this class, as opposed to having the web app do we game
    # TODO - create dummy funcs for the things app.py reference the game_manager for. Make everything else _
    # TODO - set up some cool enum structure that defines the round? E.g. draw, discard etc. with conditions on when to progress?

    """

    def __init__(self, scorer: Scorer = None) -> None:
        self.scorer = scorer
        self.has_not_taken_turn = self.scorer.players.copy()
        # TODO - Remove current player? Orr use it more? Maybe easier than having to check the UID all the time
        self.current_player = self._get_next_player()
        self.game_phase = GameState.CHOOSE_WHAT_TO_DRAW
        self.num_cards_drawn_current_turn = 0
        self.selected_card_to_play = None
        # self.players ... (one day :-))
        print(f"I have been created with players {self.scorer.players}")

    def start_next_round(self):
        """
        Checks if the game is over - if not switch to the next player so they can take their turn
        """
        self.game_phase = GameState.CHOOSE_WHAT_TO_DRAW
        self.num_cards_drawn_current_turn = 0
        self.selected_card_to_play = None
        self.current_player = self._get_next_player()

    def is_game_over(self):
        """
        Returns true if the game is over (i.e. deck is empty). Otherwise returns false.
        """
        return True if self.get_amt_of_cards_left() <= 0 else False

    def _get_next_player(self):
        """
        Returns the next player instance to take its turn. All players take one turn in a pre-determined order,
        and then it goes back to the first player
        """
        if len(self.has_not_taken_turn) == 0:
            # Everybody has taken their turn - resetting to new round
            self.has_not_taken_turn = self.scorer.players.copy()
        return self.has_not_taken_turn.pop()

    def get_winner(self):
        winners, top_paths = self.scorer.determine_winner()
        return winners, top_paths

    def get_player_instance(self, name: str) -> Player:
        """
        Takes a player's name as input and returns the Player instance corresponding with that name
        This assumes player names are unique, which they currently are since they are
        assigned as Player 1, Player 2 etc.
        """
        # TODO - try to move self.scorer.players to gm
        for p in self.scorer.players:
            if name == p.name:
                return p
        else:
            raise ValueError(f"Tried finding instance of {name}, but it didn't exist in {self.scorer.players}")

    def get_amt_of_cards_left(self) -> int:
        # TODO - refactor this? Could assign the deck as a gm class var, but would duplicate?
        print(f"returning {self.scorer.players[0].deck.get_amt_of_cards_left()}")
        return self.scorer.players[0].deck.get_amt_of_cards_left()

    def select_card_to_play(self, card_name: str) -> None:
        # Note - selected_card_to_play is shared across users since it's reset ahead of each turn
        self.selected_card_to_play = card_name
        self.game_phase = GameState.CHOOSE_WHERE_TO_PLAY

    def draw_card(self, player_name: str, to_draw_from: str = None):
        player = self.get_player_instance(player_name)

        if to_draw_from:
            # Drawing from a discard pile
            player_to_draw_from = self.get_player_instance(to_draw_from)
            player.draw_card_from_discard(player_to_draw_from=player_to_draw_from)
        else:
            # Drawing from the deck
            player.draw_card_from_deck()

        self.num_cards_drawn_current_turn += 1
        if self.num_cards_drawn_current_turn >= 2:
            # If the player has drawn two cards the game moves on to the play card phase
            self.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    def discard_card(self, player_name: str, card_to_discard: str):
        player = self.get_player_instance(player_name)

        player.discard_card(card_to_discard, to_discard=True)
        print("Checking if game is over")
        if self.is_game_over():
            print("Game is over")
            self.game_phase = GameState.SCORING
        else:
            self.start_next_round()

    def play_card_at_chosen_coords(self, player_name: str, row: int, column: int):
        player = self.get_player_instance(player_name)
        try:
            player.play_card(self.selected_card_to_play, row=row, column=column)
        except ValueError as e:
            # User chose an invalid location for a card (e.g. not adjacent to an existing card)
            # - notifying user and resetting to start of play phase
            self.selected_card_to_play = None
            self.game_phase = GameState.CHOOSE_CARD_TO_PLAY
            raise e

        self.selected_card_to_play = None
        self.game_phase = GameState.CHOOSE_DISCARD


class GameState(Enum):
    # TODO - turn into str enum - easier to work with (have to upgrade Python to the latest version)
    CHOOSE_WHAT_TO_DRAW = "Draw"
    CHOOSE_CARD_TO_PLAY = "Choose Card"
    CHOOSE_WHERE_TO_PLAY = "Choose Coords"
    CHOOSE_DISCARD = "Choose Discard"
    SCORING = "Scoring"


# TODO - add messages back in using flash_io
player_game_state_messages = {
    GameState.CHOOSE_WHAT_TO_DRAW: "Draw two cards from either the deck or one of the discard piles",
    GameState.CHOOSE_CARD_TO_PLAY: "Select a card to play",
    GameState.CHOOSE_WHERE_TO_PLAY: "Select a location on the board where you want to place your card",
    GameState.CHOOSE_DISCARD: "Choose a card to discard. It will appear in your discard pile.",
    GameState.SCORING: "The game is over"
}


