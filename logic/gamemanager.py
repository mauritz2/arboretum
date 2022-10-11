from logic.player import Player
from logic.graveyard import Graveyard
from logic.deck import Deck
from logic.board import Board
from logic.scorer import Scorer
from logic.card import Card
from enum import Enum

import logic.config as config
# TODO - should all class files be changed to capital letters based on PEP?


class GameManager:

    def __init__(self, num_players: int) -> None:
        # TODO - should players be owned by GameManager or Scorer_
        self.num_players = num_players
        self.scorer = self.setup_scorer()
        self.game_over = False
        self.current_player = None
        self.game_phase = GameState.CHOOSE_WHAT_TO_DRAW
        self.num_cards_drawn_current_turn = 0
        self.selected_card_to_play = None

    def setup_scorer(self) -> Scorer:
        """
        Creates all the class instances needed to run the game, including the Scorer
        which contains all the players and their respective boards, decks, graveyards
        Returns a Scorer instance which contain all the instances to run the game
        """

        players = []
        deck = Deck()
        for i in range(self.num_players):
            player_name = f"Player {i + 1}"
            graveyard = Graveyard(cards=[])
            board = Board(num_rows=config.BOARD_ROWS, num_columns=config.BOARD_COLUMNS)

            player = Player(name=player_name,
                            deck=deck,
                            graveyard=graveyard,
                            board=board
                            )
            players.append(player)

        scorer = Scorer(players=players)
        return scorer

    def start_draw_phase(self, player) -> None:
        cards_drawn = 0
        while cards_drawn < 2:
            # Draw two cards (either from graveyard or deck)
            print("Draw a card from the deck or one of the discard piles")
            print(f"There are {len(player.deck.cards)} cards in the deck")
            print(f"The top cards in each player's discard pile is:")
            for p in self.scorer.players:
                print(f"{p.name}: {p.graveyard.get_top_card(False).card_name if p.graveyard.get_top_card(False) else None}")
            print(f"Your current hand: {player.get_player_card_names()}")
            print("Allowed messages: [1] draw deck [2] draw discard {player num} (example: draw discard 1)")

            ## CARD DRAW ##
            # TODO - clarify what card the player drew
            draw_input = input()
            if "deck" in draw_input:
                player.draw_card_from_deck()
                cards_drawn += 1
                print(f"Card drawn, there are now {len(player.deck.cards)} cards in the deck")
            elif "discard" in draw_input:
                # [-1] is the player digit from which to draw from
                target_player = draw_input[-1]
                print(f"You are drawing from the discard pile of player with number {target_player}")
                for p in self.scorer.players:
                    if target_player in p.name:
                        player.draw_card_from_graveyard(p)
                        cards_drawn += 1
                        print(
                            f"Card drawn. There are now {len(p.graveyard.cards)} card(s) in the discard pile of {p.name}. "
                            f"The new top card is {p.graveyard.get_top_card(False).card_name if p.graveyard.get_top_card(False) else None}")
                        break
                else:
                    print(f"No matching player ID found for {draw_input}. Please try again.")
            else:
                print(f"Did not recognize input {draw_input}. Please try again \n")

    def start_play_card_phase(self, player) -> None:
        print("The current board state of all players is:")
        for p in self.scorer.players:
            print(f"{p.name}:")
            p.board.print_board()
        print(f"Your current hand is {player.get_player_card_names()}")
        no_card_played = True
        ## PLAY CARD ##
        while no_card_played:
            try:
                print(f"Choose a card to play by typing it's name (example: Jacaranda 8)")
                card_to_play_input = input()
                if card_to_play_input not in player.cards_on_hand:
                    print(f"{card_to_play_input} is not a card on your hand. Please enter another card.")
                    continue
                print(f"Choose the row and column to place the card (example: 1 1)")
                row_col_input = input()
                row = int(row_col_input[0])
                column = int(row_col_input[-1])
                player.play_card(card_to_play_input, row, column)
                no_card_played = False
                print(f"Played card {card_to_play_input}")
                print(f"Your updated board is:")
                player.board.print_board()
            except ValueError as e:
                print(e)

    def start_discard_phase(self, player) -> None:
        card_not_discarded = True
        while card_not_discarded:
            try:
                print(f"Your cards on hand are: {player.get_player_card_names()}")
                print(f"Choose a card to discard by typing it's name (example: Jacaranda 8)")
                card_to_discard_input = input()
                if card_to_discard_input not in player.cards_on_hand:
                    print(f"{card_to_discard_input} is not a card on your hand. Please enter another card.")
                    continue
                player.discard_card(card_to_discard_input, to_graveyard=True)
                card_not_discarded = False
                print(f"Card discarded. Your hand is now: {player.get_player_card_names()}")
            except ValueError as e:
                print(e)

    def next_player(self):
        self.game_phase = GameState.CHOOSE_WHAT_TO_DRAW
        self.num_cards_drawn_current_turn = 0
        self.selected_card_to_play = None


class GameState(Enum):
    CHOOSE_WHAT_TO_DRAW = "Draw"
    CHOOSE_CARD_TO_PLAY = "Choose Card"
    CHOOSE_WHERE_TO_PLAY = "Choose Coords"
    CHOOSE_DISCARD = "Choose Discard"
    SCORING = "Scoring"

