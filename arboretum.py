from flask import Flask, render_template, request, redirect, url_for, flash
from logic import game_manager
from logic import GameState, player_game_state_messages

# Flask config
app = Flask(__name__)
app.secret_key = b'this-is-a-dev-env-secret-key-abc-abc'


@app.route("/", methods=["GET"])
def main():
    """
    Gets the data to display in the UI and renders the main game screen
    """
    player_boards = {}
    player_hands = {}
    top_discard_cards = {}
    for p in game_manager.scorer.players:
        player_name = p.name
        # TODO This sends a nested list with Cards() - send just the card name instead?
        player_boards[player_name] = p.board.board_grid
        player_hands[player_name] = p.get_player_card_names()
        top_discard_cards[player_name] = p.discard.get_top_card(only_str=True)

    current_player_name = game_manager.current_player.name
    game_phase = game_manager.game_phase.value
    num_cards_in_deck = game_manager.scorer.players[0].deck.get_amt_of_cards_left()

    flash(player_game_state_messages[game_manager.game_phase])
    print("Player hands!")
    print(player_boards)
    print("End of player hands")

    return render_template(
        'game.html',
        player_hands=player_hands,
        player_boards=player_boards,
        game_phase=game_phase,
        top_discard_cards=top_discard_cards,
        current_player_name=current_player_name,
        num_cards_in_deck=num_cards_in_deck,
    )


@app.route("/game_over", methods=["GET"])
def game_over():
    """
    Gets the data to display in the UI on the game over screen and then renders the page
    """
    # TODO - this is repetition with main() - break out into function?
    player_boards = {}
    player_hands = {}
    for p in game_manager.scorer.players:
        player_name = p.name
        # TODO This sends a nested list with Cards() - implement func in board to send just the card name instead?
        player_boards[player_name] = p.board.board_grid
        player_hands[player_name] = p.get_player_card_names()

    winners, top_paths = game_manager.get_winner()

    # TODO - should this be implemented as part of the scorer? It is a very specific id/coord structure
    for player in top_paths:
        for tree_dict in top_paths[player]:
            list_of_coords = []
            for card in top_paths[player][tree_dict]["Path"]:
                player_instance = game_manager.scorer.get_player_instance(player)
                (row, col) = player_instance.board.find_coords_of_card(card)
                # If is player num, row, col (e.g. 111 is Player 1 row 1 column 1)
                coords_id = str(player)[-1] + str(row) + str(col)
                list_of_coords.append(coords_id)
            top_paths[player][tree_dict]["Path"] = list_of_coords

    print(top_paths)
    print(winners)

    return render_template("game_over.html",
                           player_hands=player_hands,
                           player_boards=player_boards,
                           top_paths=top_paths,
                           winners=winners
                           )


@app.route("/draw_card_from_deck", methods=["POST"])
def draw_card_from_deck():
    """
    Draws a card from the deck and adds it to the players hand. Progresses to the next phase (i.e. play card)
    when two cards have been drawn
    # TODO - if multiplayer is implemented, check will be needed that correct player tries to perform an action
    """
    if game_manager.current_player.deck.get_amt_of_cards_left() <= 0:
        flash("The deck is empty. Scoring will start after the current turn is complete.", "error")
        return redirect(url_for("main"))

    game_manager.current_player.draw_card_from_deck()
    game_manager.num_cards_drawn_current_turn += 1
    if game_manager.num_cards_drawn_current_turn >= 2:
        game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    return redirect(url_for("main"))


@app.route("/draw_from_discard", methods=["POST"])
def draw_card_from_discard():
    """
    Draws a card from a selected discard pile and adds it to the players hand. Progresses to the next phase
    (i.e. play card) when two cards have been drawn
    """
    player_to_draw_from = request.form["discard_owner"]
    player_instance = game_manager.scorer.get_player_instance(player_to_draw_from)
    game_manager.current_player.draw_card_from_discard(player_to_draw_from=player_instance)

    game_manager.num_cards_drawn_current_turn += 1
    if game_manager.num_cards_drawn_current_turn >= 2:
        game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    return redirect(url_for("main"))


@app.route("/choose_card_to_play", methods=["POST"])
def choose_card_to_play():
    """
    Identifies the card the player has chosen to play and sets the game manager to remember the card. Then progresses
    the game state so the player can choose where to place the selected card
    """
    selected_card_to_play = request.form['card_name']
    game_manager.selected_card_to_play = selected_card_to_play
    game_manager.game_phase = GameState.CHOOSE_WHERE_TO_PLAY

    return redirect(url_for("main"))


@app.route("/choose_coordinates", methods=["POST"])
def choose_coordinates():
    """
    Gets input indicating the coordinates where the player wants to play the selected card.
    Form input format: str(row, column). Example: (1,1). Then plays the card to that location.
    Progresses to the discard phase after playing the card.
    """

    if game_manager.game_phase != GameState.CHOOSE_WHERE_TO_PLAY:
        flash(f"You can't place a card now. The current game phase is {game_manager.game_phase}.", "error")
        return redirect(url_for("main"))

    if game_manager.selected_card_to_play is None:
        flash(f"No card has been selected to be played. Select a card to play.", "error")
        return redirect(url_for("main"))

    card_to_play = game_manager.selected_card_to_play
    row, column = eval(request.form["coords"])
    row, column = int(row), int(column)

    try:
        game_manager.current_player.play_card(card_to_play, row=row, column=column)
    except ValueError as e:
        # User chose an invalid location for a card (e.g. not adjacent to an existing card)
        # - notifying user and resetting to start of play phase
        game_manager.selected_card_to_play = None
        game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY
        flash(str(e) + " Please select what card to play", "error")
        return redirect(url_for("main"))

    game_manager.selected_card_to_play = None
    game_manager.game_phase = GameState.CHOOSE_DISCARD

    return redirect(url_for("main"))


@app.route("/discard_card", methods=["POST"])
def discard_card():
    """
    Discards a chosen card from the player's hand. Then checks if the game is over (i.e. deck is empty).
    If it is, navigate to the scoring screen. If it's not, start the next player's turn.
    """
    card_to_discard = request.form["card_name"]
    game_manager.current_player.discard_card(card_to_discard, to_discard=True)

    game_over_bool = game_manager.check_if_game_is_over()

    if game_over_bool:
        game_manager.game_phase = GameState.SCORING
        return redirect(url_for("game_over"))

    game_manager.start_next_round()
    return redirect(url_for("main"))


if __name__ == "__main__":
    app.run(debug=True)
