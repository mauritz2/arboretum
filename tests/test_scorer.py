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




    # def test_establish_scorering_players_8_vs_1(player, player2, scorer):
    # 	player.trees_on_hand = ["Oak 1"]
    # 	player2.trees_on_hand = ["Oak 8"]
    # 	scorer_dict = scorer.calculate_scoring_players_by_tree()
    # 	assert len(scorer_dict["Oak"]) == 1
    # 	assert scorer_dict["Oak"][0] is player
    #
    # def _test_find_straight_path(player, scorer):
    # 	player.trees_on_hand ["Oak 2", "Cassia 5", "Oak 7"]
    # 	player.place_tree(player.trees_on_hand[0], row=0, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=1, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=1, column=1)
    # 	scorer.players=[player]
    # 	paths = scorer.find_paths(tree_type="Oak")
    # 	assert paths[0] = ["O2", "C5", "O7"]
    #
    # def _test_find_path_endpoint_coordinates(player, scorer)
    # 	player.trees_on_hand ["Oak 2", "Oak 4" "Cassia 5", "Oak 6" "Oak 7"]
    # 	player.place_tree(player.trees_on_hand[0], row=0, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=1, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=2, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=3, column=0)
    # 	player.place_tree(player.trees_on_hand[0], row=4, column=0)
    #
    # 	scorer.players=[player]
    # 	coordinates = scorer.find_potential_path_endpoint_coordinates(tree_type="Oak")
    # 	assert coordinates == [[(0,0),(1,0)],
    # 	[(0,0),(3,0)],
    # 	[(0,0),(4,0)],
    # 	[(1,0),(3,0)],
    # 	[(1,0),(4,0)],
    # 	[(3,0),(4,0)],
    #
    #
    #
    # 	# Length
    # 	# 0 -1
    # 	# O1, O2, O3, O4, O6
    #
    #
    # def _test_find_curved_path(player):
    # 	pass
    #
    # def _test_find_multiple_paths(player):
    # 	pass
    #
    #

    # test_find_top_score
    # test_find_scoring_players
    # test_sum_cards
    # test_check_if_tree_on_hand
    # test_calculate_hand_sums
    #

    # def test_no_duplicates in deck()