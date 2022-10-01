import pytest
from app import Board, Deck, Scorer, Player, Card

# TODO - add in a dict/fixture that hold all possible Card() types - they are static and have to be re-created in many tests

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
def player(board, deck):
    player = Player(name="Player 1", deck=deck, board=board)

    tree_types = ["Oak", "Oak", "Oak", "Dogwood", "Dogwood", "Dogwood", "Jacaranda"]
    tree_vals = [2, 3, 1, 6, 2, 3, 5]

    for card_name in zip(tree_types, tree_vals):
        card = Card(tree_type=card_name[0], tree_val=card_name[1])
        player.cards_on_hand[card.card_name] = card

    # Delete the cards defined in the players hand from the deck
    for card_name_hand in player.cards_on_hand.keys():
        for i, card_name_deck in enumerate(player.deck.cards):
            if card_name_hand == card_name_deck.card_name:
                del player.deck.cards[i]

    return player


@pytest.fixture
def player2(board2, deck):
    return Player(name="Player 2", deck=deck, board=board2)


@pytest.fixture
def scorer(player, player2):
    return Scorer(players=[player, player2], trees=["Cassia", "Dogwood", "Jacaranda", "Oak"])

