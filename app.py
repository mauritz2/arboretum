from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from logic import game_logic
from logic import GameState, player_game_state_messages
import json

# Flask config
app = Flask(__name__)
app.secret_key = b'this-is-a-dev-env-secret-key-abc-abc'


@app.route("/draw_card_from_deck", methods=["POST"])
def draw_card_from_deck():

    if game_logic.game_phase != GameState.CHOOSE_WHAT_TO_DRAW:
        flash(f"You can't draw cards now. The current game phase is {game_logic.game_phase}", "error")
        return redirect(url_for("main"))

    if game_logic.current_player.deck.get_amt_of_cards_left() <= 0:
        flash("The deck is empty. Scoring will start after the current turn is complete.", "error")
        return redirect(url_for("main"))

    game_logic.current_player.draw_card_from_deck()
    game_logic.num_cards_drawn_current_turn += 1
    if game_logic.num_cards_drawn_current_turn >= 2:
        game_logic.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    return redirect(url_for("main"))


@app.route("/draw_from_discard", methods=["POST"])
def draw_card_from_discard():

    if game_logic.game_phase != GameState.CHOOSE_WHAT_TO_DRAW:
        flash(f"You can't discard cards now. The current game phase is {game_logic.game_phase}", "error")
        return redirect(url_for("main"))

    player_to_draw_from = request.form["discard_owner"]

    player_instance = game_logic.scorer.get_player_instance(player_to_draw_from)
    game_logic.current_player.draw_card_from_graveyard(player_instance)

    game_logic.num_cards_drawn_current_turn += 1
    if game_logic.num_cards_drawn_current_turn >= 2:
        game_logic.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    return redirect(url_for("main"))


@app.route("/choose_coordinates", methods=["POST"])
def choose_coordinates():
    """
    Gets form input indicating the tile where the player wants to play a card. Input format: str(row, column).
    Example: (1,1)
    """

    if game_logic.game_phase != GameState.CHOOSE_WHERE_TO_PLAY:
        flash(f"You can't choose where to place a card now. The current game phase is {game_logic.game_phase}", "error")
        return redirect(url_for("main"))

    card_to_play = game_logic.selected_card_to_play
    row, column = eval(request.form["coords"])
    row, column = int(row), int(column)

    try:
        game_logic.current_player.play_card(card_to_play, row=row, column=column)
    except ValueError as e:
        # User chose an invalid place for a card - notifying user and resetting to start of play phase
        game_logic.selected_card_to_play = None
        game_logic.game_phase = GameState.CHOOSE_CARD_TO_PLAY
        flash(str(e) + " Please select what card to play", "error")
        return redirect(url_for("main"))

    game_logic.selected_card_to_play = None
    game_logic.game_phase = GameState.CHOOSE_DISCARD

    return redirect(url_for("main"))


@app.route("/discard_card", methods=["POST"])
def discard_card():
    """
    Discards a chosen card from the player's hand
    """

    if game_logic.game_phase != GameState.CHOOSE_DISCARD:
        flash(f"You can't discard a card now. The current game phase is {game_logic.game_phase}", "error")
        return redirect(url_for("main"))

    card_to_discard = request.form["card_name"]
    game_logic.current_player.discard_card(card_to_discard, to_graveyard=True)

    game_logic.next_player()

    return redirect(url_for("main"))


@app.route("/play_card", methods=["POST"])
def play_card():

    if game_logic.game_phase != GameState.CHOOSE_CARD_TO_PLAY:
        flash(f"You can't play a card now. The current game phase is {game_logic.game_phase}")
        return redirect(url_for("main"))

    selected_card_to_play = request.form['card_name']
    game_logic.selected_card_to_play = selected_card_to_play
    game_logic.game_phase = GameState.CHOOSE_WHERE_TO_PLAY

    return redirect(url_for("main"))


@app.route("/", methods=["GET"])
def main():

    # Create player boards and hand dicts
    player_boards = {}
    player_hands = {}
    top_discard_cards = {}
    for p in game_logic.scorer.players:
        player_name = p.name
        # TODO This sends a nested list with Cards() - send just the card name instead?
        player_boards[player_name] = p.board.board_grid
        player_hands[player_name] = p.get_player_card_names()
        top_discard_cards[player_name] = p.graveyard.get_top_card(only_str=True)

    # TODO - this structure is silly - the GameManager should have the .players as opposed to scorer
    current_player_name = game_logic.current_player.name
    game_logic.game_phase = GameState.SCORING
    game_phase = game_logic.game_phase.value
    print(f"The game phase is {game_phase}")

    # top_discard_cards = {"Player 1": game_logic.scorer.players[0].graveyard.get_top_card(only_str=True)}

    num_cards_in_deck = game_logic.scorer.players[0].deck.get_amt_of_cards_left()

    flash(player_game_state_messages[game_logic.game_phase])

    if game_logic.game_phase == GameState.SCORING:
        winner, scorer_by_tree, top_paths = game_logic.get_winner()
        ## Scoring code
        # pass
        # {"Player 1": {"Cassia": [(1, 1), (2, 3), (4, 5)]}}
        #print(scorer_by_tree)
        # TODO - refactor this dict so that it's {"Player 1: ["Cassia", "Jacaranda"]} and then remove this code
        scoring_players_updated = {}
        for player in ["Player 1", "Player 2"]:
            scoring_for = []
            for tree in scorer_by_tree:
                for p in scorer_by_tree[tree]:
                    if player == p.name:
                        scoring_for.append(tree)
            scoring_players_updated[player] = scoring_for
        #print("\n")
        #print(scoring_players_updated)
        print(scoring_players_updated)
        print("Top paths below \n\n")
        print(top_paths)

        for player in top_paths:
            for tree_dict in top_paths[player]:
                list_of_coords = []
                for card in top_paths[player][tree_dict]["Path"]:
                    print(card)
                    # TODO - make this dynamically call the correct player's board
                    (row, col) = game_logic.scorer.players[0].board.find_coords_of_card(card)
                    coords = str(row) + str(col)
                    list_of_coords.append(coords)
                top_paths[player][tree_dict]["Path"] = list_of_coords

        print("Updated top paths below")
        print(top_paths)

        # TODO - these type of data structures should be made available in the GameManager instead of implementing them here

        top_paths_json = jsonify(top_paths)

    return render_template(
        'game.html',
        player_hands=player_hands,
        player_boards=player_boards,
        game_phase=game_phase,
        top_discard_cards=top_discard_cards,
        current_player_name=current_player_name,
        num_cards_in_deck=num_cards_in_deck,
        scoring_players=scoring_players_updated,
        top_paths=top_paths,
        top_paths_json=json.dumps(top_paths)
    )

@app.route("/game_over", methods=["GET"])
def game_over():
    # return render_template("game_over.html")
    # Elements on the game over screen
    # Player 1 and Player 2 Boards
    # Player 1 and Player 2 Hands
    # Should show:
        # Who scored for what
        # How much they scored for that color
        # Mouse-over highlight showing the path that they scored for
    pass



if __name__ == "__main__":
    app.run(debug=True)

# Next steps
# Display amount  of cards left in deck
# Dynamic "numbers" on cards
# Cool "appear-on-hover" buttons on cards as opposed to ugly always-visible buttons
# "Display Player 2 board"
# Implement player turns - or design that system (e.g. does the front-end AND backend know whos turn it is?
# I think the backend can know - or must know. And it passes this information to the front-end.


