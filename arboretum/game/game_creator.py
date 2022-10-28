import arboretum.game.config as config
from arboretum.game.logic.player import Player
from arboretum.game.logic.discard import Discard
from arboretum.game.logic.deck import Deck
from arboretum.game.logic.board import Board
from arboretum.game.logic.scorer import Scorer
from arboretum.game.game_manager import GameManager


def get_tree_types(num_players: int) -> list[str]:
    """
    Returns the trees to use in the game, e.g. the names and the amount
    """
    num_trees = config.AMT_TREES_PER_AMT_PLAYER[num_players]
    return config.TREES[:num_trees]


def create_game(player_names: list[str]) -> GameManager:
    """
    Creates all the class instances needed to run the game and returns the GameManager
    instance
    """
    players = []
    tree_types = get_tree_types(len(player_names))

    deck = Deck(tree_types=tree_types, num_cards_per_type=config.CARDS_PER_TREE_TYPE)

    for player_name in player_names:
        discard = Discard(cards=[])
        board = Board(num_rows=config.BOARD_ROWS, num_columns=config.BOARD_COLUMNS)
        player = Player(name=player_name, deck=deck, discard=discard, board=board)
        players.append(player)

    scorer = Scorer(players=players, trees=tree_types)
    game_manager = GameManager(scorer=scorer)
    return game_manager
