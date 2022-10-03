import player
from player import Player
from board import Board
from deck import Deck
from scorer import Scorer
from card import Card
from graveyard import Graveyard
from gamemanager import GameManager
import config


def main():
    # TODO - change graveyard to discard pile naming consistently
    # TODO - break out into separate game manager methods (e.g. draw_phase, play_card_phase) for readability
    game_manager = GameManager(config.NUM_PLAYERS)
    while not game_manager.game_over:
        # Players take turns to take action
        for player in game_manager.scorer.players:
            print("\n\n")
            print(f"Start of turn for: {player.name}")
            ### DRAW PHASE ####
            ## SETUP ##
            cards_drawn = 0
            while cards_drawn < 2:
                # Draw two cards (either from graveyard or deck)
                print("Draw a card from the deck or one of the discard piles")
                print(f"There are {len(player.deck.cards)} cards in the deck")
                print(f"The top cards in each player's discard pile is:")
                for p in game_manager.scorer.players:
                    print(f"{p.name}: {p.graveyard.get_top_card().card_name}")
                print("Allowed messages: [1] draw deck [2] draw discard {player num} (example: draw discard 1)")

                ## CARD DRAW ##
                draw_input = input()
                if "deck" in draw_input:
                    player.draw_card_from_deck()
                    cards_drawn += 1
                    print(f"Card drawn, there are now {len(player.deck.cards)} cards in the deck")
                elif "discard" in draw_input:
                    # [-1] is the player digit from which to draw from
                    target_player = draw_input[-1]
                    print(f"You are drawing from the discard pile of player with number {target_player}")
                    for p in game_manager.scorer.players:
                        if target_player in p.name:
                            player.draw_card_from_graveyard(p)
                            cards_drawn += 1
                            print(
                                f"Card drawn. There are now {len(p.graveyard.cards)} card(s) in the discard pile of {p.name}. "
                                f"The new top card is {p.graveyard.get_top_card().card_name if p.graveyard.get_top_card() else None}")
                            break
                    else:
                        print(f"No matching player ID found for {draw_input}. Please try again.")
                else:
                    print(f"Did not recognize input {draw_input}. Please try again \n")

            ### PLAY CARD PHASE ####
            ## SETUP ##
            print("The current board state of all players is:")
            for p in game_manager.scorer.players:
                print(f"{p.name}:")
                p.board.print_board()
            print(f"Your current hand is {list(player.cards_on_hand.keys())}")
            no_card_played = True
            ## PLAY CARD ##
            while no_card_played:
                try:
                    print(f"Choose a card to play by typing it's name (example: Jacaranda 8)")
                    card_to_play_input = input()
                    if card_to_play_input not in player.cards_on_hand:
                        print(f"{card_to_play_input } is not a card on your hand. Please enter another card.")
                        continue
                    print(f"Choose the row and column to place the card (example: 1 1)")
                    row_col_input = input()
                    row = int(row_col_input[0])
                    column = int(row_col_input[-1])
                    player.place_tree(card_to_play_input, row, column)
                    no_card_played = False
                    print(f"Played card {card_to_play_input}")
                    print(f"Your updated board is:")
                    player.board.print_board()
                except ValueError as e:
                    print(e)

            ### DISCARD CARD PHASE ####
            card_not_discarded = True
            while card_not_discarded:
                try:
                    print(f"Your cards on hand are: {list(player.cards_on_hand.keys())}")
                    print(f"Choose a card to discard by typing it's name (example: Jacaranda 8)")
                    card_to_discard_input = input()
                    if card_to_discard_input not in player.cards_on_hand:
                        print(f"{card_to_discard_input} is not a card on your hand. Please enter another card.")
                        continue
                    player.discard_card(card_to_discard_input, to_graveyard=True)
                    card_not_discarded = False
                    print(f"Card discarded. Your hand is now: {list(player.cards_on_hand.keys())}")
                except ValueError as e:
                    print(e)

            ### CHECK IF GAME IS OVER PHASE ###
            if player.deck.check_amt_of_cards_left() <= 0:
                print("\nThe game is over - scoring begins\n")
                game_manager.game_over = True
                quit()

    # Determine the winner
    print("The game is over!")


if __name__ == "__main__":
    main()
