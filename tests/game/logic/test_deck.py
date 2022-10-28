import pickle
from arboretum.game.logic.card import Card


def test_shuffle_deck(deck):
    """
    Verify that the card order is different pre- and post-shuffle
    """
    pre_shuffle_pickle = pickle.dumps(deck.cards)
    deck.shuffle_deck()
    post_shuffle_pickle = pickle.dumps(deck.cards)
    assert pre_shuffle_pickle != post_shuffle_pickle


def test_generate_deck(deck):
    """
    Verify deck gets correct size and is made up of Card instances
    """
    assert len(deck.cards) == 64
    assert type(deck.cards) == list
    assert isinstance(deck.cards[0], Card)
    for card in deck.cards:
        assert card.tree_num in range(1, 9)


def test_get_top_card(deck):
    """
    Verify deck gets correct size and is made up of Card instances
    """
    top_card = deck.cards[-1]
    top_card_actual = deck.get_top_card()
    assert top_card == top_card_actual

    deck.cards = []
    top_card_empty_deck = deck.get_top_card()
    assert top_card_empty_deck is None


def test_remove_top_card(deck):
    """
    Verify we can get top card
    """
    top_card = deck.get_top_card()
    deck.remove_top_card()
    assert top_card != deck.get_top_card()


def test_get_amt_of_cards_left(deck):
    """
    Verify we can get amount of cards left
    """
    assert deck.get_amt_of_cards_left() == 64
    deck.remove_top_card()
    assert deck.get_amt_of_cards_left() == 63
