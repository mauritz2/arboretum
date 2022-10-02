import player
from player import Player
from board import Board
from deck import Deck
from scorer import Scorer
from card import Card
from graveyard import Graveyard
from gamemanager import GameManager
import config
import sys

def main():
	game_manager = GameManager(config.NUM_PLAYERS)
	while not game_manager.game_over:
		for player in game_manager.scorer.players:
			# Players take turns to take action

			# Draw two cards (either from graveyard or deck)
			print("Draw two cards from deck or one of the discard piles")
			print(player.)
			draw_response = input()
			print(draw_response)
			if draw_response == "Draw deck":
				player.draw_card_from_deck()

			quit()
			# elif

			# else:


			# Play one card

			# Discard one card

			# Check if the game is over (i.e. someone drew the last card in the deck)
			# TODO - might indicate bad design where there are so many nested instances - what could improve this?
			if game_manager.scorer.player.deck.check_amt_of_cards_left() <= 0:
				game_manager.game_over = True

	# Determine the winner
	print("The game is over!")


if __name__ == "__main__":
	main()
