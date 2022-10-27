from arboretum.game.logic.card import Card
from tests.game.conftest import cards as c


def test_find_paths_single_simple_path(scorer):
    scorer.players[0].board.board_grid[2][2] = c["Oak 2"]
    scorer.players[0].board.board_grid[2][3] = c["Cassia 4"]
    scorer.players[0].board.board_grid[2][4] = c["Jacaranda 6"]
    scorer.players[0].board.board_grid[2][5] = c["Oak 7"]

    player = scorer.players[0]

    path = scorer.find_paths_for_tree_type("Oak", player)
    path_expected = [[c["Oak 2"], c["Cassia 4"], c["Jacaranda 6"], c["Oak 7"]]]

    assert path == path_expected


def test_find_paths_two_simple_paths(scorer):
    # Path start
    scorer.players[0].board.board_grid[2][2] = c["Oak 2"]

    # Path #1
    scorer.players[0].board.board_grid[2][3] = c["Cassia 4"]
    scorer.players[0].board.board_grid[2][4] = c["Jacaranda 6"]

    # Path #2
    scorer.players[0].board.board_grid[3][2] = c["Blue Spruce 3"]
    scorer.players[0].board.board_grid[3][3] = c["Blue Spruce 4"]
    scorer.players[0].board.board_grid[3][4] = c["Blue Spruce 6"]
    scorer.players[0].board.board_grid[3][5] = c["Blue Spruce 7"]

    # Path end
    scorer.players[0].board.board_grid[2][5] = c["Oak 8"]

    player = scorer.players[0]

    path = scorer.find_paths_for_tree_type("Oak", player)
    path_expected = [[c["Oak 2"], c["Blue Spruce 3"], c["Blue Spruce 4"], c["Blue Spruce 6"], c["Blue Spruce 7"], c["Oak 8"]],
                     [c["Oak 2"], c["Cassia 4"], c["Jacaranda 6"], c["Oak 8"]]]

    path.sort()
    path_expected.sort()

    assert path == path_expected


def test_find_paths_short_medium_long(scorer):
    # Path start
    scorer.players[0].board.board_grid[2][2] = c["Oak 2"]

    # Path #1 #2 #3
    scorer.players[0].board.board_grid[1][2] = c["Blue Spruce 3"]
    scorer.players[0].board.board_grid[0][2] = c["Cassia 4"]
    scorer.players[0].board.board_grid[0][3] = c["Jacaranda 6"]
    scorer.players[0].board.board_grid[1][3] = c["Blue Spruce 7"]

    # Path end
    scorer.players[0].board.board_grid[2][3] = c["Oak 8"]

    player = scorer.players[0]

    path = scorer.find_paths_for_tree_type("Oak", player)
    path_expected = [[c["Oak 2"], c["Oak 8"]],
                     [c["Oak 2"], c["Blue Spruce 3"], c["Blue Spruce 7"], c["Oak 8"]],
                     [c["Oak 2"], c["Blue Spruce 3"], c["Cassia 4"], c["Jacaranda 6"], c["Blue Spruce 7"], c["Oak 8"]]]
    path.sort()
    path_expected.sort()

    assert path == path_expected


def test_find_paths_branching_paths(scorer):
    """
    Verify that we can find all paths when paths branch out multiple times
    """
    # Path start
    scorer.players[0].board.board_grid[0][0] = c["Oak 2"]

    # Original path
    scorer.players[0].board.board_grid[1][0] = c["Blue Spruce 3"]
    scorer.players[0].board.board_grid[2][0] = c["Oak 4"]

    # Branch # 1
    scorer.players[0].board.board_grid[1][1] = c["Blue Spruce 5"]
    scorer.players[0].board.board_grid[1][2] = c["Blue Spruce 6"]
    scorer.players[0].board.board_grid[1][3] = c["Oak 7"]

    # Branch 2
    scorer.players[0].board.board_grid[2][2] = c["Oak 8"]

    player = scorer.players[0]

    path = scorer.find_paths_for_tree_type("Oak", player)
    path_expected = [[c["Oak 2"], c["Blue Spruce 3"], c["Oak 4"]],
                     [c["Oak 2"], c["Blue Spruce 3"], c["Blue Spruce 5"], c["Blue Spruce 6"], c["Oak 7"]],
                     [c["Oak 2"], c["Blue Spruce 3"], c["Blue Spruce 5"], c["Blue Spruce 6"], c["Oak 8"]]]
    path.sort()
    path_expected.sort()

    assert path == path_expected


def test_get_possible_start_end_loc_pairs(scorer):
    """
    Verify that we get all valid start/end permutations that can make up a path
    """
    oak1 = c["Oak 1"]
    oak2 = c["Oak 2"]
    oak4 = c["Oak 4"]
    oak8 = c["Oak 8"]

    cards = [oak1, oak2, oak4, oak8]

    expected_combos = [
        (oak1, oak2),
        (oak1, oak4),
        (oak1, oak8),
        (oak2, oak4),
        (oak2, oak8),
        (oak4, oak8),
    ]
    start_end_combos = scorer.get_possible_start_end_card_pairs(cards)

    start_end_combos.sort()
    expected_combos.sort()

    assert start_end_combos == expected_combos


def test_get_possible_start_end_loc_pairs_empty(scorer):
    """
    Verify we get an empty list if there are no permutation
    """
    assert scorer.get_possible_start_end_card_pairs([]) == []


def test_score_paths_3_paths_and_ending_in_8(scorer):
    """
    Verify scoring is accurate with three paths, all ending in 8 (i.e. +2 points)
    """
    paths = [[c["Oak 2"], c["Oak 8"]],
             [c["Oak 2"], c["Blue Spruce 3"], c["Blue Spruce 7"], c["Oak 8"]],
             [c["Oak 2"], c["Blue Spruce 3"], c["Cassia 4"], c["Jacaranda 6"], c["Blue Spruce 7"], c["Oak 8"]]]

    expected_best_path = [c["Oak 2"], c["Blue Spruce 3"], c["Cassia 4"], c["Jacaranda 6"], c["Blue Spruce 7"], c["Oak 8"]]
    # 6 from path length, 2 from ending on an 8
    expected_score = 8

    top_path, score = scorer._score_paths(paths)
    assert top_path == expected_best_path
    assert score == expected_score


def test_score_path_complex(scorer):
    """
    Verify scoring of path where all trees are the same (i.e. double points) and that starts with 1
    (+1 point) and ends with 8 (+2 points)
    """

    paths = [[c["Oak 1"], c["Oak 3"], c["Oak 4"], c["Oak 8"]]]

    expected_best_path = [c["Oak 1"], c["Oak 3"], c["Oak 4"], c["Oak 8"]]

    # +8 from path length (all Oaks), +1 from starting with 1, +2 from ending on an 8
    expected_score = 11

    top_path, score = scorer._score_paths(paths)
    assert top_path == expected_best_path
    assert score == expected_score


def test_determine_winner_one_tree_one_path_each(scorer):
    """
    Verify  that player 1 wins when they are the only ones that
    can score for their Oak path. Note that player 2's Oak 8 is negated by player 1's Oak 1
    """

    # Player 1 hand
    scorer.players[0].cards_on_hand = {
        "Oak 1": c["Oak 1"],
        "Oak 2": c["Oak 2"]
    }

    # Player 1 path - 3
    scorer.players[0].board.board_grid[1][2] = c["Oak 3"]
    scorer.players[0].board.board_grid[1][3] = c["Oak 4"]
    scorer.players[0].board.board_grid[1][4] = c["Oak 5"]

    # Player 2 hand
    scorer.players[1].cards_on_hand = {
        "Oak 8": c["Oak 8"],
    }

    # Player 2 path - not scoring
    scorer.players[1].board.board_grid[1][2] = c["Oak 6"]
    scorer.players[1].board.board_grid[1][3] = c["Oak 7"]

    winner, _ = scorer.determine_winner()
    assert winner == ["Player 1"]


def test_determine_winner_multiple_trees_and_paths(scorer):
    """
    Verify that player 2 wins when they have one great path vs. player two's two
    less good scoring paths
    """

    # Player 1 hand
    scorer.players[0].cards_on_hand = {
        "Oak 1": c["Oak 1"],
        "Oak 2": c["Oak 2"],
        "Blue Spruce 4": c["Blue Spruce 4"]
    }

    # Player 1 path
    # Oak Path -> 3
    # Blue Spruce Path -> 3
    scorer.players[0].board.board_grid[1][2] = c["Oak 3"]
    scorer.players[0].board.board_grid[1][3] = c["Blue Spruce 4"]
    scorer.players[0].board.board_grid[1][4] = c["Oak 4"]
    scorer.players[0].board.board_grid[1][5] = c["Blue Spruce 6"]

    # Player 2 hand
    scorer.players[1].cards_on_hand = {
        "Oak 8": c["Oak 8"],
    }

    # Player 2 path
    # Jac path -> 8
    # Oak path -> Not scoring
    scorer.players[1].board.board_grid[1][0] = c["Jacaranda 1"]
    scorer.players[1].board.board_grid[1][1] = c["Jacaranda 2"]
    scorer.players[1].board.board_grid[1][2] = c["Oak 6"]
    scorer.players[1].board.board_grid[1][3] = c["Oak 7"]
    scorer.players[1].board.board_grid[1][4] = c["Jacaranda 8"]

    winner, _ = scorer.determine_winner()
    assert winner == ["Player 2"]


def test_determine_winner_tie(scorer):
    """
    Verify that player 2 wins when they have one great path vs. player two's two
    less good scoring paths
    """

    # Player 1 hand
    scorer.players[0].cards_on_hand = {
        "Oak 1": c["Oak 1"],
        "Oak 2": c["Oak 2"],
        "Blue Spruce 4": c["Blue Spruce 4"]
    }

    # Player 1 path
    # Oak Path -> 3
    # Blue Spruce Path -> 3
    scorer.players[0].board.board_grid[1][2] = c["Oak 3"]
    scorer.players[0].board.board_grid[1][3] = c["Blue Spruce 4"]
    scorer.players[0].board.board_grid[1][4] = c["Oak 5"]
    scorer.players[0].board.board_grid[1][5] = c["Blue Spruce 6"]


    # Player 2 hand
    scorer.players[1].cards_on_hand = {
        "Oak 8": c["Oak 8"],
    }

    # Player 2 path
    # Jac path -> 8
    scorer.players[1].board.board_grid[1][0] = c["Jacaranda 2"]
    scorer.players[1].board.board_grid[1][1] = c["Jacaranda 3"]
    scorer.players[1].board.board_grid[1][2] = c["Oak 7"]
    scorer.players[1].board.board_grid[1][3] = c["Jacaranda 8"]

    winner, _ = scorer.determine_winner()
    assert winner == ["Player 1", "Player 2"]


def test_calculate_scoring_players(player, player2, scorer):
    player.cards_on_hand = {}
    tree_types_1 = ["Cassia", "Cassia", "Oak", "Jacaranda", "Jacaranda"]
    tree_vals_1 = [4, 3, 8, 1, 7]
    for card_name in zip(tree_types_1, tree_vals_1):
        card = Card(tree_type=card_name[0], tree_num=card_name[1])
        player.cards_on_hand[card.name] = card

    player2.cards_on_hand = {}
    tree_types_2 = ["Oak", "Cassia", "Jacaranda"]
    tree_vals_2 = [1, 7, 8]
    for card_name in zip(tree_types_2, tree_vals_2):
        card = Card(tree_type=card_name[0], tree_num=card_name[1])
        player2.cards_on_hand[card.name] = card

    scorer.players = [player, player2]

    expected_dict = {"Player 1": ["Cassia", "Jacaranda", "Blue Spruce"], "Player 2": ["Cassia", "Blue Spruce",  "Oak"]}
    actual_dict = scorer.calculate_scoring_players()
    for p_name in ["Player 1", "Player 2"]:
        actual = actual_dict[p_name]
        actual.sort()
        expected = expected_dict[p_name]
        expected.sort()
        assert(actual == expected)


def test_establish_scoring_players_empty_hands(player, player2, scorer):
    player.cards_on_hand = {}
    player2.cards_on_hand = {}
    players = [player, player2]
    scorer.players = players

    scorer.trees = ["Cassia", "Blue Spruce", "Jacaranda", "Lilac", "Magnolia", "Maple", "Olive"]

    expected_dict = {"Player 1": ["Cassia", "Blue Spruce", "Jacaranda", "Lilac", "Magnolia", "Maple", "Olive"], "Player 2": ["Cassia", "Blue Spruce", "Jacaranda", "Lilac", "Magnolia", "Maple", "Olive"]}
    actual_dict = scorer.calculate_scoring_players()

    for p_name in ["Player 1", "Player 2"]:
        for p_name in ["Player 1", "Player 2"]:
            actual = actual_dict[p_name]
            actual.sort()
            expected = expected_dict[p_name]
            expected.sort()
            assert (actual == expected)