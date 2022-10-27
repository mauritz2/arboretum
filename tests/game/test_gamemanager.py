import pytest


def test_get_next_player_id(gamemanager, player, player2):
    """
    Verify that we get the correct player ids
    """
    player_1 = gamemanager.get_next_player_id([])
    assert player_1 == "Player 1"
    player_2 = gamemanager.get_next_player_id([player.name])
    assert player_2 == "Player 2"
    player_3 = gamemanager.get_next_player_id([player2.name])
    assert player_3 == "Player 1"


def test_get_next_player_id_adding_too_many(gamemanager, player, player2):
    """
    Verify that we can't generate more ids for players than the num of players
    Num players in the gamemanager fixture is 2
    """
    with pytest.raises(ValueError):
        gamemanager.get_next_player_id([player.name, player2.name])

