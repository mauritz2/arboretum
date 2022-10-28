from arboretum.game import game_creator


def test_generate_deck():
    tree_types = game_creator.get_tree_types(num_players=2)
    assert len(tree_types) == 6

    tree_types = game_creator.get_tree_types(num_players=3)
    assert len(tree_types) == 8
