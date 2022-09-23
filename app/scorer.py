import random

import config
from card import Card


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

    def find_potential_path_endpoint_coordinates(self):
        pass

    # Create a dict with structure O2: (0, 1)
    # Loop through this dict and find

    def find_paths(self):

        paths = []
        # TODO - change to run for all trees
        valid_paths = []

        for tree in ["Oak"]:
            cards_of_type = self.board.get_played_cards_of_type(tree)
            start_end_combos = self.get_possible_start_end_card_pairs()

            for start_end_combo in start_end_combos:
                current_path = []
                adjacencies = self.board.find_adjacent_incrementing_cards(start_end_combo[0])

                while len(next_adjacencies) > 0:
                    # This is not deterministic - this is why we have to run many times to make sure we get all the paths
                    current_adjacency = random.choice(adjacencies)
                    current_path.append(current_adjacency)
                    if current_adjacency == start_end_combos[1]:
                        valid_paths.append(current_path)

                next_adjacencies = self.board.find_adjacent_incrementing_cards(current_adjacency)


                # FindAllPaths (not deterministic - loop through 100 times to find "all" paths)
                # Start at the start square
                # Try going in all directions and put them in a list
                # For each entry in the list
                # Is it a blank (i.e. no card) - if so remove from options and break
                # Check if its not incrementing - if so remove from options break
                # Check if the card isn't used elsewhere in this path (i.e. loop) - if so remove from options and break
                # If the cell is the destination cell and the length is above 3 - append to paths
                # If no options remains - return paths
                # If multiple ones remain - pick a random one
                # Record the card as taken for this specific path
                # return FindAllPaths() on the new cell!!!
        return valid_paths