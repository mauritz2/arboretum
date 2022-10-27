from tests.game.conftest import cards as c


def test_get_top_card(discard):
    """
    Verify that name of top card can be retrieved
    """
    assert discard.get_top_card(only_str=True) == "Cassia 2"


def test_remove_top_card(discard):
    """
    Verify that top card can be removed
    """
    assert discard.cards[-1].name == "Cassia 2"
    discard.remove_top_card()
    assert discard.cards[-1].name == "Cassia 1"


def test_add_card_on_top(discard):
    """
    Verify that discarded cards get put on top
    """
    assert discard.cards[-1].name == "Cassia 2"
    discard.add_card_on_top(c["Cassia 8"])
    assert discard.cards[-1].name == "Cassia 8"


def test_get_amt_of_cards_remaining(discard):
    """
    Verify that we can get amount of remaining cards in discard
    """
    assert discard.get_amt_of_cards_remaining() == 2
    discard.add_card_on_top(c["Cassia 8"])
    assert discard.get_amt_of_cards_remaining() == 3
