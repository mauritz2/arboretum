import random

import game.config as config
from game.logic.card import Card
from game.logic.player import Player


class Scorer:
    """
    Class to determine who scores and how much.
    This class holds the players in the game.
    """
    def __init__(self, players: list[Player], trees: list[str] = None):
        self.players = players
        self.trees = config.TREES if trees is None else trees

    def calculate_scoring_players(self) -> dict[str: list[str]]:
        """
        Determines who scores based on the sum of the cards on each player's hand at the end of the game
        Multiple players can score for each type of tree, if the sum of the cards in their hand is equal for
        that tree type
        As per the rules, if a player has an 8, but another player has the 1 of the same tree type, the 8 counts as 0

        Returns the format below:
        {"Player 1": ["Cassia", "Jacaranda", "Blue Spruce", "Oak"], "Player 2": ["Cassia", "Blue Spruce"]}
        """
        scoring_players = {}

        for tree_type in self.trees:
            top_tree_score = 0
            scorers = []
            for player in self.players:
                # Calculate the total sum for the current tree type (e.g. Oak)
                cards = player.cards_on_hand.values()
                card_values = [card.tree_num if card.tree_type == tree_type else 0 for card in cards]
                score = sum(card_values)

                # Make 8 count as 0, if an opposing player has the 1 with that same tree type
                if 8 in card_values:
                    one_card_name = Card(tree_type=tree_type, tree_num=1).name
                    if self.is_in_opponents_hand(one_card_name, player_to_excl=player.name):
                        score -= 8

                # Check if the total sum for this tree is the highest, or tied with highest
                if score > top_tree_score:
                    top_tree_score = score
                    scorers = [player.name]
                elif score == top_tree_score:
                    scorers.append(player.name)
            # This loop is used to make the player the key in the return dict, which matches most other scoring dicts
            for scorer in scorers:
                if scorer in scoring_players:
                    scoring_players[scorer].append(tree_type)
                else:
                    scoring_players[scorer] = [tree_type]

        return scoring_players

    def is_in_opponents_hand(self, card_name: str, player_to_excl: str) -> bool:
        """
        Check if a specific tree (e.g. Oak 8) exists in the hand of any players
        This is used to find if any players have 1s to negate the 8s when evaluating who scores
        Returns True if the specified card exists, otherwise returns False
        """
        for player in self.players:
            if player.name == player_to_excl:
                continue
            if card_name in player.cards_on_hand:
                return True
        return False

    @staticmethod
    def get_possible_start_end_card_pairs(cards_of_type: list[Card]) -> list[tuple]:
        """
        Takes as input a list with all played Cards of a specific type (e.g. Oak) and returns
        a list of tuples containing the possible start/end Cards that could start/end a path
        This is later used in path finding to check if there's an actual path between start and end
        """
        start_end_combos = []
        for card in cards_of_type:
            for comparison_card in cards_of_type:
                if card.tree_num < comparison_card.tree_num:
                    start_end_combo = (card, comparison_card)
                    start_end_combos.append(start_end_combo)

        return start_end_combos

    def find_paths_for_tree_type(self, tree_type: str, player: Player) -> list[list[Card]]:
        """
        Finds all the valid paths for a specific tree type on a player's board and returns
        a list where each entry is a list with a valid path. Each step in the path is represented
        by its Card instance

        Steps to get all the paths:
        1. Find all the played cards of a specific type (e.g. Oak)
        2. Generate all possible valid combos, e.g. Oak 1 could be start card and Oak 3 could be an end card. But
        Oak 3 could never be a start and Oak 1 an end since each card in a path needs to have an incremental value.
        3. Loop through all the possible start-end pairs
        4. For each start card - find all adjacent cards with higher values than the center card (i.e. possible path)
        5. Repeat finding new adjacencies for all identified adjacencies. Stop if you reach the end card.
        If you find it you have a valid path. If you didn't find it,
        no path exists between this start and end combination.
        """
        valid_paths = []
        cards_of_type = player.board.get_played_cards_of_type(tree_type)
        start_end_combos = self.get_possible_start_end_card_pairs(cards_of_type=cards_of_type)

        # TODO - make this deterministic (i.e. we need to know when all possible paths have been traversed)
        # Keeping thoughts below for traceability:
        # The main challenge is knowing when all paths have been traversed
        # Even if at each time there are multiple valid adjacencies we check which path we took last time, and take
        # the other route, that wouldn't ensure we pick all paths.
        # Because the path could be branching again further out.
        # We could try to keep a dict of all the intersections that we find and store them in a dict. And then go back
        # to them and indicate when everything has been followed? Maybe that's the best approach
        # Then change the for i in range(20) to a while loop that tracks whether all options at crossroads
        # have been followed. What's the best data structure to keep track of the cross-roads?
        # {cross_road_tuple: {adj_tuple:traversed_bool} --> {"(1,1"): {"1,1": True, ... }
        # We would need a function is_any_crossroad_unexplored() that traverses this dict and finds any remaining
        # Still we will end up looping through many times to find all the paths...
        # Not a great solution either. Leaving this as-is for now. Most commonly there are no branches
        # And with 20 iterations through the tree, if there's one branch the probability of not finding it would be
        # 0.5^20 = 9.53674316e-7. If there would be a million games played that would be an issue, but don't see that
        # happening. If it is, either we'd need to make this deterministic or increase 20 to a higher number.

        for i in range(20):
            for start_end_combo in start_end_combos:
                # Start the path with the starting card
                current_path = [start_end_combo[0]]

                # Find the coordinates of the start card and then all adjacent incrementing cards
                row_num, col_num = player.board.find_coords_of_card(start_end_combo[0])
                next_adjs = player.board.get_adjacent_cards(row=row_num, column=col_num, ignore_tree_num=False)

                # Continue until there are no more incremental adjacencies (i.e. no path continuation)
                while len(next_adjs) > 0:
                    # TODO - refactor to remove this non-determinism (see comments above)
                    current_adjacency = random.choice(next_adjs)
                    current_path.append(current_adjacency)
                    if current_adjacency == start_end_combo[1]:
                        if current_path not in valid_paths:
                            # We've found a valid path that we haven't found before
                            valid_paths.append(current_path)
                            break
                    # If path not valid yet, find next set of adjacencies to continue building path
                    row_num, col_num = player.board.find_coords_of_card(current_adjacency)
                    next_adjs = player.board.get_adjacent_cards(row=row_num, column=col_num, ignore_tree_num=False)

        return valid_paths

    @staticmethod
    def _score_paths(paths_to_score: list[list[Card]]) -> (list[Card], int):
        """
        Takes a list of lists containing all valid paths and calculates the score for the top scoring path
        Returns the top scoring path, and it's related score
        """
        top_path = []
        top_score = 0

        for path in paths_to_score:
            path_score = 0

            # Player gets 1 point for each card in the path
            path_score += len(path)

            # If the path starts with a 1 the player gets +1 point
            if path[0].tree_num == 1:
                path_score += 1

            # If path ends in 8 the player gets +2 points
            if path[-1].tree_num == 8:
                path_score += 2

            # Player gets 1 additional point for each card in the path if the path is at least 4 cards
            # long and all cards in the path are of the same species.
            tree_types = [card.tree_type for card in path]
            all_tree_types_same = [tree_types[0]] * len(path) == tree_types
            if all_tree_types_same and len(path) >= 4:
                path_score += len(path)

            # Check if the current path is the best one
            if path_score > top_score:
                top_score = path_score
                top_path = path

        return top_path, top_score

    def determine_winner(self) -> (list[str], dict[str, dict]):
        """
        Determines what player won by determining who scores for each tree, and then calculating path scores
        Returns the scoring player
        # TODO - implement better draw rules - e.g. player that can play the highest card from their hand wins
        # if scores are tied
        """
        top_paths = {}
        winning_score = 0
        winners = []

        scoring_players = self.calculate_scoring_players()
        for player in self.players:
            score_by_tree = {}
            for tree in self.trees:
                if tree not in scoring_players[player.name]:
                    # Score = None indicates the player did not score for this path
                    # This distinction between a score of 0 and None is useful because when
                    # visualizing in the UI the top_paths dict can show who scored,
                    # with what path, and what the score was
                    score_by_tree[tree] = {"Path": [], "Score": None}
                else:
                    # The player scored - calculate the highest-scoring path and add it to the total
                    paths = self.find_paths_for_tree_type(tree, player)
                    top_path, top_score = self._score_paths(paths)
                    score_by_tree[tree] = {"Path": top_path, "Score": top_score}
                    player.score += top_score
            else:
                top_paths[player.name] = score_by_tree
                if player.score > winning_score:
                    winning_score = player.score
                    winners = [player.name]
                elif player.score == winning_score:
                    winners.append(player.name)
        return winners, top_paths
