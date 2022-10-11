from flask import Flask, render_template, request, redirect, url_for, flash
from logic import game_logic
from logic import GameState

# Flask config
app = Flask(__name__)
app.secret_key = b'this-is-a-dev-env-secret-key-abc-abc'
app.config['DEBUG'] = False


@app.route("/draw_card_from_deck", methods=["POST"])
def draw_card_from_deck():

    if game_logic.game_phase != GameState.CHOOSE_WHAT_TO_DRAW:
        flash(f"You can't draw cards now. The current game phase is {game_logic.game_phase}")
        return redirect(url_for("main"))

    game_logic.scorer.players[0].draw_card_from_deck()
    game_logic.num_cards_drawn_current_turn += 1
    if game_logic.num_cards_drawn_current_turn >= 2:
        game_logic.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    return redirect(url_for("main"))


@app.route("/draw_from_discard", methods=["POST"])
def draw_card_from_discard():

    if game_logic.game_phase != GameState.CHOOSE_WHAT_TO_DRAW:
        flash(f"You can't discard cards now. The current game phase is {game_logic.game_phase}")
        return redirect(url_for("main"))

    player_to_draw_from = request.form["discard_owner"]
    player_instance = game_logic.scorer.get_player_instance(player_to_draw_from)
    game_logic.scorer.players[0].draw_card_from_graveyard(player_instance)

    game_logic.num_cards_drawn_current_turn += 1
    if game_logic.num_cards_drawn_current_turn >= 2:
        game_logic.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    return redirect(url_for("main"))

@app.route("/choose_coordinates", methods=["POST"])
def choose_coordinates():
    """
    Gets form input from the tile selected by the user in the format row, column (e.g. 1,1)
    """

    if game_logic.game_phase != GameState.CHOOSE_WHERE_TO_PLAY:
        flash(f"You can't choose where to place a card now. The current game phase is {game_logic.game_phase}")
        return redirect(url_for("main"))

    card_to_play = game_logic.selected_card_to_play
    row, column = eval(request.form["coords"])

    row, column = int(row), int(column)
    # TODO - refactor so players[0] references the player that clicked the button
    game_logic.scorer.players[0].play_card(card_to_play, row=row, column=column)

    game_logic.selected_card_to_play = None

    game_logic.game_phase = GameState.CHOOSE_DISCARD

    return redirect(url_for("main"))


@app.route("/discard_card", methods=["POST"])
def discard_card():
    """
    Discards a chosen card from the player's hand
    """

    if game_logic.game_phase != GameState.CHOOSE_DISCARD:
        flash(f"You can't discard a card now. The current game phase is {game_logic.game_phase}")
        return redirect(url_for("main"))

    card_to_discard = request.form["card_name"]
    game_logic.scorer.players[0].discard_card(card_to_discard, to_graveyard=True)

    game_logic.next_player()

    return redirect(url_for("main"))


@app.route("/play_card", methods=["POST"])
def play_card():

    if game_logic.game_phase != GameState.CHOOSE_CARD_TO_PLAY:
        flash(f"You can't play a card now. The current game phase is {game_logic.game_phase}")
        return redirect(url_for("main"))

    # Verify that the game state is playing a card!
    # if not game_logic.current_game_state == "Draw"
        # raise ValueError("It's not time to draw"
    # If not request.form.player == game_logic.current_player:
        # raise ValueError("It's not your time to play!")
    # Check who the player is
    #player_name = request.form.player
    selected_card_to_play = request.form['card_name']

    game_logic.selected_card_to_play = selected_card_to_play
    game_logic.game_phase = GameState.CHOOSE_WHERE_TO_PLAY

    return redirect(url_for("main"))


@app.route("/", methods=["GET"])
def main(message=None):

    player_hand = game_logic.scorer.players[0].get_player_card_names()
    player_hands = {"Player 1": player_hand}

    player_board = game_logic.scorer.players[0].board.board_grid
    player_boards = {"Player 1": player_board}

    #current_players_turn = game_logic.current_player

    top_discard_cards = {"Player 1": game_logic.scorer.players[0].graveyard.get_top_card(only_str=True)}

    game_phase = game_logic.game_phase.value

    flash(game_logic.game_phase)

    return render_template(
        'main.html',
        player_hands=player_hands,
        player_boards=player_boards,
        game_phase=game_phase,
        top_discard_cards=top_discard_cards,
        message=message

    )


if __name__ == "__main__":
    app.run(debug=True)

# Next steps
# Display amount  of cards left in deck
# Dynamic "numbers" on cards
# Cool "appear-on-hover" buttons on cards as opposed to ugly always-visible buttons