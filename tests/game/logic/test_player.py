import pytest
from tests.game.conftest import cards as c


def test_place_tree(player):
    """
    Verify that placing a card places it on the board at the designated coords
    """
    player.play_card(card_name="Oak 1", row=0, column=1)
    assert player.board.board_grid[0][1] == c["Oak 1"]


def test_place_tree_not_in_hand(player):
    """
    Verify you can't play a card not in your hand
    """
    with pytest.raises(ValueError):
        player.play_card(card_name="Oak 75", row=0, column=1)


def test_place_same_card_twice(player):
    """
    Verify that played cards get removed from the player's hand
    """
    card_name = "Oak 1"
    row, column = 0, 1
    player.play_card(card_name, row, column)
    with pytest.raises(ValueError):
        player.play_card(card_name, row, column)


def test_place_card_in_occupied_space(player):
    """
    Verify that it's not possible to play a card on top of another card on the board
    """
    card_1 = "Oak 1"
    card_2 = "Oak 2"
    row, column = 0, 1
    player.play_card(card_1, row, column)
    with pytest.raises(ValueError):
        player.play_card(card_2, row, column)


def test_add_drawn_card_to_hand(player):
    """
    Verify drawn cards are added to the player's hand
    """
    card_to_draw = player.deck.get_top_card().name
    assert card_to_draw not in player.cards_on_hand
    player.draw_card_from_deck()
    assert card_to_draw in player.cards_on_hand


def test_remove_drawn_card_from_deck(player):
    """
    Verify that drawn cards get removed from the deck
    """
    card_to_draw = player.deck.get_top_card()
    assert card_to_draw in player.deck.cards
    player.draw_card_from_deck()
    assert card_to_draw not in player.deck.cards


def test_reject_no_adjacency(player):
    """
    Verify that it's not possible to place cards that are not adjacent to an existing card
    (given that it's not the first card played during the game)
    """
    card = "Oak 2"
    row, column = 0, 1
    player.first_tree_placed = True
    with pytest.raises(ValueError):
        player.play_card(card, row, column)


def test_reject_no_adjacency_diagonal_tree(player):
    """
    Verify that cards placed diagonally to another card aren't considered as adjacencies
    """
    card_1 = "Oak 1"
    card_2 = "Oak 2"
    row1, column1 = 0, 0
    row2, column2 = 1, 1
    player.play_card(card_1, row1, column1)
    with pytest.raises(ValueError):
        player.play_card(card_2, row2, column2)


def test_draw_card_from_discard(player):
    """
    Verify that drawing from a discard pile removes the card from the discard pile and adds it to the player's hand
    """
    # discard contains Cassia 1 and Cassia 2 by default with Cassia 2 as the top card
    assert "Cassia 2" not in player.cards_on_hand
    assert "Cassia 2" in [crd.name for crd in player.discard.cards]
    player.draw_card_from_discard(player)
    assert "Cassia 2" in player.cards_on_hand
    assert "Cassia 2" not in [crd.name for crd in player.discard.cards]


def test_draw_card_from_discard_draw_from_other_player(player, player2):
    """
    Verify that drawing from other players' discard piles works
    """
    player2.discard.cards = [c["Jacaranda 8"]]
    player.draw_card_from_discard(player2)
    assert "Jacaranda 8" in player.cards_on_hand.keys()
    assert "Jacaranda 8" not in [crd.name for crd in player2.discard.cards]
