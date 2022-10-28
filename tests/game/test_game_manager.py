
def test_get_next_player(game_manager):
    assert game_manager._get_next_player().name == "Player 1"
    assert game_manager._get_next_player().name == "Player 2"
