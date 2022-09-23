import config
from card import Card

class Scorer:
	def __init__(self, players:list, trees: list = None):
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
							some_player_has_1 = self._check_if_tree_on_hand(tree, "1")
							if some_player_has_1:
								print(f"A player has the 1 of {tree} - this 8 will be disregarded")
								break
						total_sum += card.tree_val
				player_sum_by_tree[tree] = total_sum
			hand_sums[player] = player_sum_by_tree

		return hand_sums

	def _check_if_tree_on_hand(self, tree_type:str, tree_num:str):
		# TODO - refactor this
		card = tree_type + " " + tree_num
		for player in self.players:
			if card in player.cards_on_hand:
				return True
		return False


	def _find_top_score(self, scorer_dict:dict, tree:str) -> int:
		"""
		Find the top hand sum of a specified tree
		"""
		top_score = 0
		for player in scorer_dict:
			score = scorer_dict[player][tree]
			if score > top_score:
				top_score = score
		return top_score

	def _find_scoring_players(self, scorer_dict:dict, top_score:int, tree:str) -> list:
		"""
		Find the players that have a score equal to the top score for a specified tree
		"""
		top_scorers = []
		for player in scorer_dict:
			if scorer_dict[player][tree] == top_score:
				top_scorers.append(player)
		return top_scorers

	def find_potential_path_endpoint_coordinates():
		pass
		# Create a dict with structure O2: (0, 1)
		# Loop through this dict and find 

	def find_paths(tree_type):
		raise NotImplementedError
		# TODO Things I need before implementing
		# 1. filter_board function (board function)
		# 2. get_adjacent (board function)
		# 3. find_and_score_paths()
		# 4. find_paths_recursively()


		# For each card_type in config.TREES:
			# start_end = board.get_all_cards_of_type(card_type)


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