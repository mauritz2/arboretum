import random

import config
from card import Card
from player import Player


class Scorer:
    def __init__(self, players: list, trees: list = None):
        self.players = players
        self.trees = config.TREES if trees is None else trees

    def calculate_scoring_players_by_tree(self):
        scorers_by_tree = {}
        hand_sums = self._calculate_hand_sums()
        for tree in self.trees:
            top_score = self._find_top_score(hand_sums, tree)
            top_scorers = self._find_scoring_players(hand_sums, top_score, tree)
            # TODO - refactor so that player name is dict and then value is a list of trees they scored for?
            # might be more natural to loop through players when tallying up scores
            scorers_by_tree[tree] = top_scorers
        return scorers_by_tree

    def _calculate_hand_sums(self):
        """
		Calculates the sum of the cards on each player's hand
		Example: the sum of [Oak 2, Oak 3] is 5
		"""
        hand_sums = {}
        for player in self.players:
            player_sum_by_tree = {}
            hand = player.cards_on_hand
            for tree in self.trees:
                total_sum = 0
                for card_name, card in hand.items():
                    if card.tree_type == tree:
                        if card.tree_val == 8:
                            print(f"A player has the 8 of {tree}")
                            another_player_has_the_1 = self._check_if_tree_on_hand(tree_type=tree,
                                                                                   tree_num=1,
                                                                                   player_to_excl=player.name)
                            if another_player_has_the_1:
                                print(f"A player has the 1 of {tree} - this 8 will be disregarded")
                                continue
                        total_sum += card.tree_val
                player_sum_by_tree[tree] = total_sum
            hand_sums[player] = player_sum_by_tree

        return hand_sums

    def _check_if_tree_on_hand(self, tree_type: str, tree_num: int, player_to_excl: list[str]):
        card = tree_type + " " + str(tree_num)
        for player in self.players:
            if player.name == player_to_excl:
                break
            if card in player.cards_on_hand:
                return True
        return False

    def _find_top_score(self, scorer_dict: dict, tree: str) -> int:
        """
		Find the top hand sum of a specified tree
		"""
        top_score = 0
        for player in scorer_dict:
            score = scorer_dict[player][tree]
            if score > top_score:
                top_score = score
        return top_score

    def _find_scoring_players(self, scorer_dict: dict, top_score: int, tree: str) -> list:
        """
		Find the players that have a score equal to the top score for a specified tree
		"""
        top_scorers = []
        for player in scorer_dict:
            if scorer_dict[player][tree] == top_score:
                top_scorers.append(player)
        return top_scorers

    @staticmethod
    def get_possible_start_end_card_pairs(cards_of_type:list[Card]) -> list[tuple]:
        """
        Takes as input a list with all played Cards of a specific type (e.g. Oak) and returns
        a list of tuples containing the possible start/end Cards that could start/end a path
        This is later used in path finding to check if there's an actual path between start and end
        """
        start_end_combos = []
        for card in cards_of_type:
            for comparison_card in cards_of_type:
                if card.card_name == comparison_card.card_name:
                    continue
                if card.tree_val < comparison_card.tree_val:
                    start_end_combo = (card, comparison_card)
                    start_end_combos.append(start_end_combo)

        return start_end_combos


    def find_paths_for_tree_type(self, tree_type:str, player:Player) -> list[Card]:
        """

        """
        valid_paths = []
        cards_of_type = player.board.get_played_cards_of_type(tree_type)
        start_end_combos = self.get_possible_start_end_card_pairs(cards_of_type=cards_of_type)

        # TODO - make this deterministic (i.e. we need to know when all possible paths have been traversed)
        for i in range(20):
            for start_end_combo in start_end_combos:
                # Start the path with the starting card
                current_path = [start_end_combo[0]]

                # Find the coordinates of the start card and then all adjacent incrementing cards
                row_num, col_num = player.board.find_coords_of_card(start_end_combo[0])
                next_adjs = player.board.find_adj_increment_cards(
                    row=row_num, column=col_num)

                # Continue until there are no more incremental adjacencies (i.e. no path continuation)
                while len(next_adjs) > 0:
                    # TODO - refactor to remove this non-determinism - func has to know when all paths have been found
                    current_adjacency = random.choice(next_adjs)
                    current_path.append(current_adjacency)
                    if current_adjacency == start_end_combo[1]:
                        if current_path not in valid_paths:
                            # We have reached the targeted end card - we've found a valid path
                            valid_paths.append(current_path)
                            break
                    # If path not valid yet, find next set of adjacencies to continue building path
                    row_num, col_num = player.board.find_coords_of_card(current_adjacency)
                    next_adjs = player.board.find_adj_increment_cards(row=row_num, column=col_num)

        return valid_paths

    def score_game(self):
        for player in self.players:
            for tree in config.TREES:
                paths = self.find_paths_for_tree_type(tree, player)

