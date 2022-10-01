from app import Card


def test_establish_scoring_players_simple_case(player, player2, scorer):
    player.cards_on_hand = {}
    tree_types_1 = ["Oak", "Oak", "Cassia", "Dogwood", "Dogwood", "Dogwood", "Jacaranda"]
    tree_vals_1 = [2, 3, 5, 6, 2, 3, 5]
    for card_name in zip(tree_types_1, tree_vals_1):
        card = Card(tree_type=card_name[0], tree_val=card_name[1])
        player.cards_on_hand[card.card_name] = card

    player2.cards_on_hand = {}
    tree_types_2 = ["Oak", "Cassia", "Dogwood", "Dogwood", "Jacaranda"]
    tree_vals_2 = [8, 8, 4, 5, 7]
    for card_name in zip(tree_types_2, tree_vals_2):
        card = Card(tree_type=card_name[0], tree_val=card_name[1])
        player2.cards_on_hand[card.card_name] = card

    scorer.players = [player, player2]
    scorer_dict = scorer.calculate_scoring_players_by_tree()
    assert scorer_dict["Cassia"][0] is player2
    assert scorer_dict["Dogwood"][0] is player
    assert scorer_dict["Jacaranda"][0] is player2
    assert scorer_dict["Oak"][0] is player2


def test_establish_scoring_players_both_score(player, player2, scorer):
    player.cards_on_hand = {}
    tree_types_1 = ["Oak", "Oak", "Cassia", "Cassia"]
    tree_vals_1 = [2, 3, 5, 2]
    for card_name in zip(tree_types_1, tree_vals_1):
        card = Card(tree_type=card_name[0], tree_val=card_name[1])
        player.cards_on_hand[card.card_name] = card

    player2.cards_on_hand = {}
    tree_types_2 = ["Oak", "Cassia"]
    tree_vals_2 = [5, 7]
    for card_name in zip(tree_types_2, tree_vals_2):
        card = Card(tree_type=card_name[0], tree_val=card_name[1])
        player2.cards_on_hand[card.card_name] = card

    scorer.players = [player, player2]
    scorer_dict = scorer.calculate_scoring_players_by_tree()
    assert player in scorer_dict["Cassia"]
    assert player2 in scorer_dict["Cassia"]
    assert player in scorer_dict["Oak"]
    assert player2 in scorer_dict["Oak"]


def test_establish_scoring_players_empty_hands(player, player2, scorer):
    player.cards_on_hand = {}
    player2.cards_on_hand = {}
    players = [player, player2]
    scorer.players = players
    scorer.trees = ["Cassia", "Dogwood", "Jacaranda", "Lilac", "Magnolia", "Maple", "Olive"]
    scorer_dict = scorer.calculate_scoring_players_by_tree()
    for p in players:
        assert p in scorer_dict["Cassia"]
        assert p in scorer_dict["Dogwood"]
        assert p in scorer_dict["Jacaranda"]
        assert p in scorer_dict["Lilac"]
        assert p in scorer_dict["Magnolia"]
        assert p in scorer_dict["Maple"]
        assert p in scorer_dict["Olive"]


def test_find_paths_single_simple_path(scorer):
    oak2 = Card(tree_type="Oak", tree_val=2)
    cas4 = Card(tree_type="Cassia", tree_val=4)
    jac6 = Card(tree_type="Jacaranda", tree_val=6)
    oak7 = Card(tree_type="Oak", tree_val=7)

    scorer.players[0].board.board_grid[2][2] = oak2
    scorer.players[0].board.board_grid[2][3] = cas4
    scorer.players[0].board.board_grid[2][4] = jac6
    scorer.players[0].board.board_grid[2][5] = oak7

    player = scorer.players[0]

    path = scorer.find_paths_for_tree_type("Oak", player)
    path_expected = [[oak2, cas4, jac6, oak7]]

    assert path == path_expected


def test_find_paths_two_simple_paths(scorer):
    oak2 = Card(tree_type="Oak", tree_val=2)
    cas4 = Card(tree_type="Cassia", tree_val=4)
    dog3 = Card(tree_type="Dogwood", tree_val=3)
    dog4 = Card(tree_type="Dogwood", tree_val=4)
    dog6 = Card(tree_type="Dogwood", tree_val=6)
    jac6 = Card(tree_type="Jacaranda", tree_val=6)
    dog7 = Card(tree_type="Dogwood", tree_val=7)
    oak8 = Card(tree_type="Oak", tree_val=8)

    # Path start
    scorer.players[0].board.board_grid[2][2] = oak2

    # Path #1
    scorer.players[0].board.board_grid[2][3] = cas4
    scorer.players[0].board.board_grid[2][4] = jac6

    # Path #2
    scorer.players[0].board.board_grid[3][2] = dog3
    scorer.players[0].board.board_grid[3][3] = dog4
    scorer.players[0].board.board_grid[3][4] = dog6
    scorer.players[0].board.board_grid[3][5] = dog7

    # Path end
    scorer.players[0].board.board_grid[2][5] = oak8

    player = scorer.players[0]

    path = scorer.find_paths_for_tree_type("Oak", player)
    path_expected = [[oak2, dog3, dog4, dog6, dog7, oak8],
                     [oak2, cas4, jac6, oak8]]

    path.sort()
    path_expected.sort()

    assert path == path_expected


def test_find_paths_short_medium_long(scorer):
    oak2 = Card(tree_type="Oak", tree_val=2)
    cas4 = Card(tree_type="Cassia", tree_val=4)
    dog3 = Card(tree_type="Dogwood", tree_val=3)
    jac6 = Card(tree_type="Jacaranda", tree_val=6)
    dog7 = Card(tree_type="Dogwood", tree_val=7)
    oak8 = Card(tree_type="Oak", tree_val=8)

    # Path start
    scorer.players[0].board.board_grid[2][2] = oak2

    # Path #1 #2 #3
    scorer.players[0].board.board_grid[1][2] = dog3
    scorer.players[0].board.board_grid[0][2] = cas4
    scorer.players[0].board.board_grid[0][3] = jac6
    scorer.players[0].board.board_grid[1][3] = dog7

    # Path end
    scorer.players[0].board.board_grid[2][3] = oak8

    player = scorer.players[0]

    path = scorer.find_paths_for_tree_type("Oak", player)
    path_expected = [[oak2, oak8],
                     [oak2, dog3, dog7, oak8],
                     [oak2, dog3, cas4, jac6, dog7, oak8]]
    path.sort()
    path_expected.sort()

    assert path == path_expected


def test_get_possible_start_end_loc_pairs(scorer):
    oak1 = Card(tree_type="Oak", tree_val=1)
    oak2 = Card(tree_type="Oak", tree_val=2)
    oak4 = Card(tree_type="Oak", tree_val=4)
    oak8 = Card(tree_type="Oak", tree_val=8)

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
    assert scorer.get_possible_start_end_card_pairs([]) == []


def test_score_paths_3_paths_and_ending_in_8(scorer):
    oak2 = Card(tree_type="Oak", tree_val=2)
    cas4 = Card(tree_type="Cassia", tree_val=4)
    dog3 = Card(tree_type="Dogwood", tree_val=3)
    jac6 = Card(tree_type="Jacaranda", tree_val=6)
    dog7 = Card(tree_type="Dogwood", tree_val=7)
    oak8 = Card(tree_type="Oak", tree_val=8)

    paths = [[oak2, oak8],
             [oak2, dog3, dog7, oak8],
             [oak2, dog3, cas4, jac6, dog7, oak8]]

    expected_best_path = [oak2, dog3, cas4, jac6, dog7, oak8]
    # 6 from path length, 2 from ending on an 8
    expected_score = 8

    top_path, score = scorer.score_paths(paths)
    assert top_path == expected_best_path
    assert score == expected_score

def test_score_path_all_same_tree_type_and_starts_with_1(scorer):
    oak1 = Card(tree_type="Oak", tree_val=1)
    oak3 = Card(tree_type="Oak", tree_val=3)
    oak4 = Card(tree_type="Oak", tree_val=4)
    oak5 = Card(tree_type="Oak", tree_val=5)
    oak6 = Card(tree_type="Oak", tree_val=6)
    oak7 = Card(tree_type="Oak", tree_val=7)

    paths = [[oak1, oak3, oak4, oak5, oak6, oak7]]

    expected_best_path = [oak1, oak3, oak4, oak5, oak6, oak7]

    # 12 from path length (all Oaks), 1 from starting with 1
    expected_score = 13

    top_path, score = scorer.score_paths(paths)
    assert top_path == expected_best_path
    assert score == expected_score


def test_determine_winner_one_tree_one_path_each(scorer):
    """
    Verify  that player 1 wins when they are the only ones that
    can score for their Oak path
    """
    oak1 = Card(tree_type="Oak", tree_val=1)
    oak2 = Card(tree_type="Oak", tree_val=2)
    oak3 = Card(tree_type="Oak", tree_val=3)
    oak4 = Card(tree_type="Oak", tree_val=4)
    oak5 = Card(tree_type="Oak", tree_val=5)
    oak6 = Card(tree_type="Oak", tree_val=6)
    oak7 = Card(tree_type="Oak", tree_val=7)
    oak8 = Card(tree_type="Oak", tree_val=8)

    # Player 1 hand
    scorer.players[0].cards_on_hand = {
        "Oak 1": oak1,
        "Oak 2": oak2
    }

    # Player 1 path
    scorer.players[0].board.board_grid[1][2] = oak3
    scorer.players[0].board.board_grid[1][3] = oak4
    scorer.players[0].board.board_grid[1][4] = oak5

    # Player 2 hand
    scorer.players[1].cards_on_hand = {
        "Oak 8": oak8,
    }

    # Player 2 path
    scorer.players[1].board.board_grid[1][2] = oak6
    scorer.players[1].board.board_grid[1][3] = oak7

    winner = scorer.determine_winner()
    assert winner.name == "Player 1"


def test_determine_winner_multiple_trees_and_paths(scorer):
    """
    Verify  that player 2 wins when they have one great path vs. player two's two
    less good scoring paths
    """
    oak1 = Card(tree_type="Oak", tree_val=1)
    oak2 = Card(tree_type="Oak", tree_val=2)
    oak3 = Card(tree_type="Oak", tree_val=3)
    oak5 = Card(tree_type="Oak", tree_val=5)
    oak6 = Card(tree_type="Oak", tree_val=6)
    oak7 = Card(tree_type="Oak", tree_val=7)
    oak8 = Card(tree_type="Oak", tree_val=8)
    dog4 = Card(tree_type="Dogwood", tree_val=4)
    dog6 = Card(tree_type="Dogwood", tree_val=6)
    jac1 = Card(tree_type="Jacaranda", tree_val=1)
    jac2 = Card(tree_type="Jacaranda", tree_val=2)
    jac8 = Card(tree_type="Jacaranda", tree_val=8)

    # Player 1 hand
    scorer.players[0].cards_on_hand = {
        "Oak 1": oak1,
        "Oak 2": oak2,
        "Dog 4": dog4
    }

    # Player 1 path
    # Oak Path -> 4
    # Dogwood Path -> 3
    scorer.players[0].board.board_grid[1][2] = oak3
    scorer.players[0].board.board_grid[1][3] = dog4
    scorer.players[0].board.board_grid[1][4] = oak5
    scorer.players[0].board.board_grid[1][5] = dog6


    # Player 2 hand
    scorer.players[1].cards_on_hand = {
        "Oak 8": oak8,
    }

    # Player 2 path
    # Jac path -> 8
    # Oath path -> Not scoring
    scorer.players[1].board.board_grid[1][0] = jac1
    scorer.players[1].board.board_grid[1][1] = jac2
    scorer.players[1].board.board_grid[1][2] = oak6
    scorer.players[1].board.board_grid[1][3] = oak7
    scorer.players[1].board.board_grid[1][4] = jac8

    winner = scorer.determine_winner()
    assert winner.name == "Player 2"
