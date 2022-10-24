import logic.config as config
from logic.player import Player
from logic.discard import Discard
from logic.deck import Deck
from logic.board import Board
from logic.scorer import Scorer
from logic.game_manager import GameManager


class GameCreator:
    """
    Takes the player names as input, sets up the game, and returns the game manager to manage the game
    """

    @staticmethod
    def create_game(player_names: list[str]) -> GameManager:
        """
        Creates all the class instances needed to run the game and returns the GameManager
        instance
        # TODO - validate player names on the front-end? E.g. no spaces etc.
        """

        players = []
        deck = Deck()

        for player_name in player_names:
            discard = Discard(cards=[])
            board = Board(num_rows=config.BOARD_ROWS, num_columns=config.BOARD_COLUMNS)
            player = Player(name=player_name, deck=deck, discard=discard, board=board)
            players.append(player)

        scorer = Scorer(players=players)
        game_manager = GameManager(scorer=scorer)
        return game_manager

