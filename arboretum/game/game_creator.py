import arboretum.game.config as config
from arboretum.game.logic.player import Player
from arboretum.game.logic.discard import Discard
from arboretum.game.logic.deck import Deck
from arboretum.game.logic.board import Board
from arboretum.game.logic.scorer import Scorer
from arboretum.game.game_manager import GameManager


class GameCreator:
    """
    Takes the player names as input, sets up the game, and returns the game manager to manage the game
    """

    @staticmethod
    def create_game(player_names: list[str]) -> GameManager:
        """
        Creates all the class instances needed to run the game and returns the GameManager
        instance
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

