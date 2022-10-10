import pytest
from logic import Card


def test_place_tree(player):
    tree = "Oak 1"
    row, column = 0, 1
    player.play_card(tree, row, column)
    assert player.board.board_grid[0][1] == Card(tree_type="Oak",
                                                 tree_val=1)


def test_place_tree_not_in_hand(player):
    tree = "Oak 75"
    row, column = 0, 1
    with pytest.raises(ValueError):
        player.play_card(tree, row, column)


def test_place_same_card_twice(player):
    tree = "Oak 1"
    row, column = 0, 1
    player.play_card(tree, row, column)
    with pytest.raises(ValueError):
        player.play_card(tree, row, column)


def test_place_card_in_occupied_space(player):
    tree1 = "Oak 1"
    tree2 = "Oak 2"
    row, column = 0, 1
    player.play_card(tree1, row, column)
    with pytest.raises(ValueError):
        player.play_card(tree2, row, column)


def test_add_drawn_card_to_hand(player):
    card_to_draw = player.deck.cards[0].card_name
    assert card_to_draw not in player.cards_on_hand
    player.draw_card_from_deck()
    assert card_to_draw in player.cards_on_hand


def test_remove_drawn_card_from_deck(player):
    card_to_draw = player.deck.cards[0]
    assert card_to_draw in player.deck.cards
    player.draw_card_from_deck()
    assert card_to_draw not in player.deck.cards


def test_reject_no_adjacency(player):
    tree = "Oak 2"
    row, column = 0, 1
    player.first_tree_placed = True
    with pytest.raises(ValueError):
        player.play_card(tree, row, column)


def test_reject_no_adjacency_diagnoal_tree(player):
    tree1 = "Oak 1"
    tree2 = "Oak 2"
    row1, column1 = 0, 0
    row2, column2 = 1, 1
    player.play_card(tree1, row1, column1)
    with pytest.raises(ValueError):
        player.play_card(tree2, row2, column2)


def test_draw_card_from_graveyard(player):
    """
    Test that drawing from a discard pile removes the card from the discard pile and adds it to the player's hand
    """
    # Graveyard contains Cassia 1 and Cassia 2 by default with Cassia 2 as the top card
    assert "Cassia 2" not in player.cards_on_hand
    assert "Cassia 2" in [c.card_name for c in player.graveyard.cards]
    player.draw_card_from_graveyard(player)
    assert "Cassia 2" in player.cards_on_hand
    assert "Cassia 2" not in [c.card_name for c in player.graveyard.cards]


def test_draw_card_from_graveyard_draw_from_other_player(player, player2):
    """
    Verify that drawing from other players' discard piles works
    """
    player2.graveyard.cards = [Card(tree_type="Jacaranda", tree_val=8)]
    player.draw_card_from_graveyard(player2)
    assert "Jacaranda 8" in player.cards_on_hand.keys()
    assert "Jacaranda 8" not in [c.card_name for c in player2.graveyard.cards]


