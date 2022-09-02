from player import Player
from board import Board
from deck import Deck
from scorer import Scorer
import config

if __name__ == "__main__":
	board = Board()
	board2 = Board()
	deck = Deck()
	player = Player("Player 1", deck, board)
	player.place_tree(player.trees_on_hand[0], row=4, column=5)
	player.place_tree(player.trees_on_hand[0], row=4, column=6)
	player2 = Player("Player 2", deck, board2)
	print(f"Player hand is {player.trees_on_hand}")
	print(f"Player 2 hand is {player2.trees_on_hand}")
	scorer = Scorer([player, player2])
	print(scorer.calculate_scoring_players_by_tree())

