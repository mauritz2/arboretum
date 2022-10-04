import pickle


def test_shuffle_deck(deck):
    pre_shuffle_pickle = pickle.dumps(deck.cards)
    deck.shuffle_deck()
    post_shuffle_pickle = pickle.dumps(deck.cards)
    assert pre_shuffle_pickle != post_shuffle_pickle
