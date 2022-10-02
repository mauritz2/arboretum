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
			print("\n\n")
			print(f"Start of turn for: {player.name}")
			print("Draw two cards from deck or one of the discard piles")
			print(f"There are {len(player.deck.cards)} cards in the deck")
			print("Allowed messages: [1] draw deck [2] draw graveyard {player num} (e.g. draw graveyard 1")
			draw_response = input()
			if draw_response == "draw deck":
				player.draw_card_from_deck()
				print(f"Card drawn, there are now {len(player.deck.cards)} cards in the deck")
			if "graveyard" in draw_response:
				# [-1] is the player digit from which to draw from
				target_player = draw_response[-1]
				for p in game_manager.scorer.players:
					if target_player in p.name:
						player.draw_card_from_graveyard(p)
						print(f"Card drawn, there are now {len(p.graveyard.cards)} cards in the graveyard of {p.name}. The top card is {p.graveyard.get_cards_remaining()}")
				else:
					print("No matching player ID found for {")


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
