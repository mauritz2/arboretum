from arboretum.game import config
from arboretum.game import game_creator


def test_generate_deck():
    deck = game_creator.create_deck(2)
    # TODO - update me once we have more cards made
    assert deck.get_amt_of_cards_left() == 48

    deck = game_creator.create_deck(3)
    # TODO - update me once we have more cards made
    assert deck.get_amt_of_cards_left() == 64

