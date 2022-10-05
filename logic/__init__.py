#import player
from logic.player import Player
from logic.board import Board
from logic.deck import Deck
from logic.scorer import Scorer
from logic.card import Card
from logic.graveyard import Graveyard
from logic.gamemanager import GameManager
import logic.config as config

# New code when Arboretum is imported

my_game = GameManager(config.NUM_PLAYERS)


# Old code to run Arboretum in the console
# def main():
#     # TODO - change graveyard to discard pile naming consistently
#     # TODO - break out into separate game manager methods (e.g. draw_phase, play_card_phase) for readability
#     game_manager = GameManager(config.NUM_PLAYERS)
#     while not game_manager.game_over:
#         # Players take turns to take action
#         for player in game_manager.scorer.players:
#             print(f"\n\n>>>> Start of turn for: {player.name}")
#             game_manager.start_draw_phase(player)
#             game_manager.start_play_card_phase(player)
#             game_manager.start_discard_phase(player)
#
#             # Check if the game is over (i.e. deck is empty)
#             # TODO - check the rules - is the player that draws the final card the last to go?
#             print("I'm assessing whether the game is over")
#             if player.deck.check_amt_of_cards_left() <= 14:
#                 print("\nThe game is over - scoring begins")
#                 game_manager.game_over = True
#                 # Break out of the player loop so no more players can act after the last card is drawn
#                 break
#     winner = game_manager.scorer.determine_winner()
#     print("The final player hands are:")
#     for p in game_manager.scorer.players:
#         # TODO - instead of doing list() and keys() this should be abstracted as a method
#         print(f"{p.name}: {list(p.cards_on_hand.keys())}")
#
#     scoring_players = game_manager.scorer.calculate_scoring_players_by_tree()
#     print("These are the scoring players for each type of tree")
#     for tree in scoring_players:
#         print(f"{tree}: {[p.name for p in scoring_players[tree]]}")
#
#     print(f"The winner is {winner.name} with {winner.score} points")
#
#     # Determine the winner
#     print("The game is over!")
#
# if __name__ == "__main__":
#     main()
