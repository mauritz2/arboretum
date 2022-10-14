from logic import Card


def test_get_top_card(discard):
    assert discard.get_top_card(False).card_name == "Cassia 2"


def test_remove_top_card(discard):
    assert discard.cards[-1].card_name == "Cassia 2"
    discard.remove_top_card()
    assert discard.cards[-1].card_name == "Cassia 1"


def test_add_card_on_top(discard):
    assert discard.cards[-1].card_name == "Cassia 2"
    discard.add_card_on_top(Card(tree_type="Cassia", tree_val=8))
    assert discard.cards[-1].card_name == "Cassia 8"


def test_get_amt_of_cards_remaining(discard):
    assert discard.get_amt_of_cards_remaining() == 2
    discard.add_card_on_top(Card(tree_type="Cassia", tree_val=8))
    assert discard.get_amt_of_cards_remaining() == 3
