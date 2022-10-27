import pytest
from arboretum.game import GameManager
from arboretum.game.logic.board import Board
from arboretum.game.logic.deck import Deck
from arboretum.game.logic.scorer import Scorer
from arboretum.game.logic.player import Player
from arboretum.game.logic.card import Card
from arboretum.game.logic.discard import Discard


@pytest.fixture
def board():
    return Board(num_rows=10, num_columns=10)


@pytest.fixture
def board2():
    return Board(num_rows=10, num_columns=10)


@pytest.fixture
def deck():
    return Deck()


@pytest.fixture
def discard():
    return Discard(
        cards=[Card(tree_type="Cassia", tree_num=1),
               Card(tree_type="Cassia", tree_num=2)]
    )


@pytest.fixture
def player(board, deck, discard):
    player = Player(name="Player 1", deck=deck, board=board, discard=discard)
    # Resetting to a blank hand to negate that player instance randomly draws cards on instantiation
    player.cards_on_hand = {}

    tree_types = ["Oak", "Oak", "Oak", "Blue Spruce", "Blue Spruce", "Blue Spruce", "Jacaranda"]
    tree_nums = [2, 3, 1, 6, 2, 3, 5]

    for card_name in zip(tree_types, tree_nums):
        card = Card(tree_type=card_name[0], tree_num=card_name[1])
        player.cards_on_hand[card.name] = card

    # Delete the cards defined in the players hand from the deck
    for card_name_hand in player.cards_on_hand.keys():
        for i, card_name_deck in enumerate(player.deck.cards):
            if card_name_hand == card_name_deck.name:
                del player.deck.cards[i]

    return player


@pytest.fixture
def player2(board2, deck, discard):
    player2 = player.Player(name="Player 2", deck=deck, board=board2, discard=discard)
    # Resetting to a blank hand to negate that player instance randomly draws cards on instantiation
    player2.cards_on_hand = {}
    return player2


@pytest.fixture
def scorer(player, player2):
    return scorer.Scorer(players=[player, player2], trees=["Cassia", "Blue Spruce", "Jacaranda", "Oak"])

@pytest.fixture
def gamemanager():
    return GameManager(2);


# Define all cards, so they can be used across test cases
cards = {}
for tree in ["Cassia", "Blue Spruce", "Jacaranda", "Oak"]:
    for num in range(8):
        card = Card(tree_type=tree, tree_num=num + 1)
        cards[card.name] = card
