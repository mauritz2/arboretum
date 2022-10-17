import pickle
from logic import Card


def test_shuffle_deck(deck):
    """
    Verifies that the card order is different pre- and post-shuffle
    """
    pre_shuffle_pickle = pickle.dumps(deck.cards)
    deck.shuffle_deck()
    post_shuffle_pickle = pickle.dumps(deck.cards)
    assert pre_shuffle_pickle != post_shuffle_pickle


def tests_generate_deck(deck):
    """
    Verify deck gets correct size and is made up of Card instances
    """
    assert len(deck.cards) == 32
    assert type(deck.cards) == list
    assert isinstance(deck.cards[0], Card)
