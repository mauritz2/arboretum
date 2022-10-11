from logic import Card


def test_get_top_card(graveyard):
    assert graveyard.get_top_card(False).card_name == "Cassia 2"


def test_remove_top_card(graveyard):
    assert graveyard.cards[-1].card_name == "Cassia 2"
    graveyard.remove_top_card()
    assert graveyard.cards[-1].card_name == "Cassia 1"


def test_add_card_on_top(graveyard):
    assert graveyard.cards[-1].card_name == "Cassia 2"
    graveyard.add_card_on_top(Card(tree_type="Cassia", tree_val=8))
    assert graveyard.cards[-1].card_name == "Cassia 8"


def test_get_amt_of_cards_remaining(graveyard):
    assert graveyard.get_amt_of_cards_remaining() == 2
    graveyard.add_card_on_top(Card(tree_type="Cassia", tree_val=8))
    assert graveyard.get_amt_of_cards_remaining() == 3
