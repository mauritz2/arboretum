from arboretum.game import config
from arboretum.game import GameCreator


def test_generate_deck():
    deck = GameCreator.create_deck(2)
    # TODO - update me once we have more cards made
    assert deck.get_amt_of_cards_left() == 24

    deck = GameCreator.create_deck(3)
    # TODO - update me once we have more cards made
    assert deck.get_amt_of_cards_left() == 32

