from player import Player
from graveyard import Graveyard
from deck import Deck
from board import Board
from scorer import Scorer
from card import Card
import config
# TODO - should all class files be changed to capital letters based on PEP?


class GameManager:

    def __init__(self, num_players: int) -> None:
        # TODO - should players be owned by GameManager or Scorer_
        self.num_players = num_players
        self.scorer = self.setup_scorer()
        self.game_over = False

    def setup_scorer(self) -> Scorer:
        """
        Creates all the class instances needed to run the game, including the Scorer
        which contains all the players and their respective boards, decks, graveyards
        Returns a Scorer instance which contain all the instances to run the game
        """

        players = []
        deck = Deck()
        for i in range(self.num_players):
            player_name = f"Player {i + 1}"
            # TODO - remove placeholder graveyard values
            graveyard = Graveyard(cards=[Card(tree_type="Oak", tree_val=1),
                                         Card(tree_type="Oak", tree_val=2)])
            board = Board(num_rows=config.BOARD_ROWS, num_columns=config.BOARD_COLUMNS)

            player = Player(name=player_name,
                            deck=deck,
                            graveyard=graveyard,
                            board=board
                            )
            players.append(player)

        scorer = Scorer(players=players)
        return scorer



