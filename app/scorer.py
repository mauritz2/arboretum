import config


class Scorer:
	def __init__(self, players:list, trees:list=config.TREES):
		self.players = players
		self.trees = trees

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
			hand = player.trees_on_hand
			for tree in self.trees:
				matching_cards = [card for card in hand if tree in card]
				total_sum = self._sum_cards(matching_cards)
					# refactor - make cards into a tuple so we can look for 8?
				if tree + " " + "8" in hand: 
					print(f"A player has the 8 of {tree}")
					some_player_has_1 = self._check_if_tree_on_hand(tree, "1")
					if some_player_has_1:
						# Card rule - having the 1 makes the 8 count as 0
						total_sum -= 8
						print(f"A player has the 1 of {tree} - new hand size is {total_sum}")
				player_sum_by_tree[tree] = total_sum
			hand_sums[player] = player_sum_by_tree
		return hand_sums

	def _check_if_tree_on_hand(self, tree_type:str, tree_num:str):
		# TODO - refactor this
		card = tree_type + " " + tree_num
		for player in self.players:
			if card in player.trees_on_hand:
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

	def _sum_cards(self, cards):
		total = 0
		for card in cards:
			total += int(card[-1])
		return total

	def find_potential_path_endpoint_coordinates():
		pass
		# Create a dict with structure O2: (0, 1)
		# Loop through this dict and find 

	def find_paths(tree_type):
		 # For each card_type in config.TREES:
			# start_end = board.get_all_cards_of_type(card_type)
			# // get combinations of start_end (i.e. at least 2 increment between start and end)

			#for combination in combinations:
				# paths = recursive(current_path=combination[0], next_cells=combination[0])

		#def recursive(current_path:list[Tile], next_cells:list[Tile], target_cell_name:Tile):
			# if next_cells.card_name = target_cell_name:
				# if len(potential_path) > 3:
					# return potential_path
				# else:
					# return None
			# incremental_adjacencies = get_incremental_adjacencies(next_cells)
			# if incremental_adjacencies == None:
				# return None

			# for each incremental_adjacency in incremental_adjacencies:
				# potential_path = recursive(incremental_adjacency)



		# potential_paths = []
		# For each start, end in possible_paths:
			# potential_paths = [[start] [start]]
			# adjacent = get_adjacent_increasing()
			# while adjacent:
				# for potential_path in potential_paths:
					# for adjacent in adjacncies:
						# potential_paths.append(adjacent)
				# current_card = adjacent
				# potential_path.append(current_card)
				# adjacent = get_adjacent_increasing()

