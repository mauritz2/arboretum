import json

import flask
import random
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit
from logic import game_manager, GameState, player_game_state_messages

# Flask config
app = Flask(__name__)
app.secret_key = b'this-is-a-dev-env-secret-key-abc-abc'
app.debug = True
app.config['SESSION_TYPE'] = "filesystem"
socketio = SocketIO(app, logger=True, manage_session=False)
# app.host="0.0.0.0"

uid_to_player_map = {}

def flash_io(text: str, category: str = "dark") -> None:
    """Send "message" to the client with the given error category"""
    emit('message', json.dumps({"text": text, "category": category}))


def emit_game_state(req) -> (dict, list[str]):
    global uid_to_player_map
    player_uid = req.cookies.get("player_uid")

    # Get the player's hand
    player_name = uid_to_player_map[player_uid]["player_id"]
    player_instance = game_manager.scorer.get_player_instance(player_name)
    cards_on_hand = player_instance.get_player_card_names()

    # Check if it's the player's turn
    current_player_name = game_manager.current_player.name

    for uid in uid_to_player_map:
        if uid_to_player_map[uid]["player_id"] == current_player_name:
            uid_name_mapping = {"uid": uid, "player_name": uid_to_player_map[uid]["player_name"]}
            print(f"The current name is {uid_to_player_map[uid]} which means UID {uid}")

    # Get the current game phase (e.g. draw, choose card to play)
    game_phase = game_manager.game_phase.value

    # Get the remaining amount of cards in the deck
    num_cards_in_deck = game_manager.scorer.players[0].deck.get_amt_of_cards_left()

    # Get top discard cards
    top_discard_cards = {}
    for p in game_manager.scorer.players:
        top_discard_cards[p.name] = p.discard.get_top_card(only_str=True)

    # Get the board for all players
    player_boards = {}
    # TODO - to think about: where is the source of truth of what players exist? GameManager?
    for uid in uid_to_player_map:
        p_instance = game_manager.scorer.get_player_instance(uid_to_player_map[uid]["player_id"])
        player_boards[uid] = p_instance.board.get_board_state()

    # Construct the game state dict
    board_state_dict = {"game_phase": game_phase,
                        "uid_name_mapping": uid_name_mapping,
                        "player_boards": player_boards,
                        "num_cards_in_deck": num_cards_in_deck,
                        "top_discard_cards": top_discard_cards}

    # Cards on hand are emitted separately since they're player-specific. The rest is public data.
    emit("update hand", json.dumps(cards_on_hand), to=request.sid)
    emit("update board state", json.dumps(board_state_dict), broadcast=True)


@socketio.on("get board state")
def get_board_state(req=None):
    if req:
        emit_game_state(req)
    else:
        emit_game_state(request)


@app.route("/lobby", methods=["GET"])
def lobby():
    # Set the player UID cookie
    response = flask.make_response(render_template("lobby.html"))
    player_uid = request.cookies.get("player_uid")
    if player_uid:
        return response

    response.set_cookie("player_uid", value=str(random.randrange(100, 999)))
    return response


@socketio.on("get player list")
def get_player_list():
    global uid_to_player_map
    emit("update player list", json.dumps(uid_to_player_map), broadcast=True)


@socketio.on('sit_down')
def on_sit_down(data):
    global uid_to_player_map
    player_uid = request.cookies.get("player_uid")
    player_name = data["player_name"]

    existing_player_ids = [value["player_id"] for value in uid_to_player_map.values()]
    print(f"\n\nThe existing player IDs are {existing_player_ids}\n\n")
    next_id = game_manager.get_next_player_id(existing_player_ids)

    uid_to_player_map[player_uid] = {"player_name": player_name, "player_id": next_id}
    print(f"\n\nUID to player map created {uid_to_player_map}\n\n")

    emit("update player list", json.dumps(uid_to_player_map), broadcast=True)
    flash_io(f"You've joined the game with name {player_name} and player ID {next_id}")


@socketio.on('stand_up')
def on_stand_up():
    global uid_to_player_map
    player_uid = request.cookies.get("player_uid")

    flash_io(
        f'Player id {uid_to_player_map[player_uid]["player_id"]} with {uid_to_player_map[player_uid]["player_name"]} has left the game.')
    del uid_to_player_map[player_uid]

    emit("update player list", json.dumps(uid_to_player_map), broadcast=True)


@socketio.on("choose card to play")
def choose_card_to_play(card_to_play):
    print(f"\n\nI am setting the card to play to {card_to_play}\n\n")
    game_manager.selected_card_to_play = card_to_play
    game_manager.game_phase = GameState.CHOOSE_WHERE_TO_PLAY
    emit_game_state(request)


@socketio.on("draw card")
def draw_card_from_deck():
    global uid_to_player_map
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]["player_id"]
    player_to_draw = game_manager.scorer.get_player_instance(player_name)
    player_to_draw.draw_card_from_deck()

    game_manager.num_cards_drawn_current_turn += 1
    if game_manager.num_cards_drawn_current_turn >= 2:
        game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    emit_game_state(request)


@socketio.on("discard card")
def discard_card(card_to_discard):
    print(f"\n\nDiscarding a card: {card_to_discard}")
    game_manager.current_player.discard_card(card_to_discard, to_discard=True)

    is_game_over = game_manager.check_if_game_is_over()

    if is_game_over:
        game_manager.game_phase = GameState.SCORING
        return redirect(url_for("game_over"))

    game_manager.start_next_round()
    emit_game_state(request)


@app.route("/game", methods=["GET"])
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

    return render_template(
        'game.html',
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


@socketio.on("draw from discard")
def draw_from_discard(player_to_draw_from):
    print(f"I am drawing from discard from {player_to_draw_from}")
    player_instance = game_manager.scorer.get_player_instance(player_to_draw_from)
    game_manager.current_player.draw_card_from_discard(player_to_draw_from=player_instance)

    game_manager.num_cards_drawn_current_turn += 1
    if game_manager.num_cards_drawn_current_turn >= 2:
        game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    emit_game_state(request)

# @app.route("/draw_from_discard_old", methods=["POST"])
# def draw_card_from_discard_old():
#     """
#     Draws a card from a selected discard pile and adds it to the players hand. Progresses to the next phase
#     (i.e. play card) when two cards have been drawn
#     """
#     player_to_draw_from = request.form["discard_owner"]
#     player_instance = game_manager.scorer.get_player_instance(player_to_draw_from)
#     game_manager.current_player.draw_card_from_discard(player_to_draw_from=player_instance)
#
#     game_manager.num_cards_drawn_current_turn += 1
#     if game_manager.num_cards_drawn_current_turn >= 2:
#         game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY
#
#     return redirect(url_for("main"))
#

@socketio.on("choose coords")
def choose_coords(chosen_coords):
    print(f"\n\nCommencing choose coords with {chosen_coords}\n\n")

    if game_manager.game_phase != GameState.CHOOSE_WHERE_TO_PLAY:
        flash(f"You can't place a card now. The current game phase is {game_manager.game_phase}.", "error")
        return redirect(url_for("main"))

    if game_manager.selected_card_to_play is None:
        flash(f"No card has been selected to be played. Select a card to play.", "error")
        return redirect(url_for("main"))

    card_to_play = game_manager.selected_card_to_play
    row = int(chosen_coords[0])
    column = int(chosen_coords[1])
    print(f"\nYou are trying to play {card_to_play} at ({row},{column})")

    try:
        game_manager.current_player.play_card(card_to_play, row=row, column=column)
        game_manager.selected_card_to_play = None
        game_manager.game_phase = GameState.CHOOSE_DISCARD
        emit_game_state(request)

    except ValueError as e:
        # User chose an invalid location for a card (e.g. not adjacent to an existing card)
        # - notifying user and resetting to start of play phase
        game_manager.selected_card_to_play = None
        game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY
        flash_io(str(e) + " Please select what card to play", "error")
        emit_game_state(request)


if __name__ == "__main__":
    socketio.run(app)
    # app.run(host="0.0.0.0")

