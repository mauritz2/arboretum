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
#Session(app)
socketio = SocketIO(app, logger=True, manage_session=False)
# app.host="0.0.0.0"

uid_to_player_map = {}

def flash_io(text: str, category: str = "dark") -> None:
    """Send "message" to the client with the given error category"""
    emit('message', json.dumps({"text": text, "category": category}))


def emit_board_state(req) -> (dict, list[str]):
    global uid_to_player_map
    #uid_to_player_map = session.get("uids")
    player_uid = req.cookies.get("player_uid")
    #board_state_dict, cards_on_hand = get_player_board_state(player_uid)
    #print("\nI got the board state dict and here it is: \n")
    #print(board_state_dict)
    #print("\n\n")

    # Get the player's hand
    player_name = uid_to_player_map[player_uid]["player_id"]
    player_instance = game_manager.scorer.get_player_instance(player_name)
    cards_on_hand = player_instance.get_player_card_names()


    # Check if it's the player's turn
    current_player_name = game_manager.current_player.name
    print(f"I will try to find {current_player_name} in {uid_to_player_map}")
    #current_player_uid = None
    #if uid_to_player_map[player_uid]["player_id"] == current_player_name:
    #    current_player_uid = uid_to_player_map[player_uid]["player_id"]

    for uid in uid_to_player_map:
       if uid_to_player_map[uid]["player_id"] == current_player_name:
           # TODO - Add the chosen player name here as well, otherwise the board can't display the real player name
           current_player_uid = uid
    else:
       if current_player_uid == None:
           raise ValueError(f"Couldn't find {current_player_uid} in {uid_to_player_map}")
    print(f"The current UID is {current_player_uid} which means {current_player_name}")

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
                        "current_player_uid": current_player_uid,
                        "player_boards": player_boards,
                        "num_cards_in_deck": num_cards_in_deck,
                        "top_discard_cards": top_discard_cards}

    # Cards on hand are emitted separately since they're player-specific. The rest is public data.
    emit("update hand", json.dumps(cards_on_hand), to=request.sid)
    emit("update board state", json.dumps(board_state_dict), broadcast=True)


@socketio.on("get board state")
def get_board_state(req=None):
    if req:
        emit_board_state(req)
    else:
        emit_board_state(request)


# def is_current_player(uid: str) -> bool:
#     global uid_to_player_map
#     print(f"I am finding out if player {uid} is the current player")
#     print(uid_to_player_map)
#     current_player_name = game_manager.current_player.name
#     if uid_to_player_map[uid]["player_id"] == current_player_name:
#         is_current_player = True
#     else:
#         is_current_player = False
#     return is_current_player


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
    #emit("update player list", json.dumps(session.get("uids")), broadcast=True)
    global uid_to_player_map
    emit("update player list", json.dumps(uid_to_player_map), broadcast=True)


@socketio.on('sit_down')
def on_sit_down(data):
    global uid_to_player_map
    #uid_to_player_map = session.get("uids")
    player_uid = request.cookies.get("player_uid")
    player_name = data["player_name"]

    # Get the player ID
    existing_player_ids = [value["player_id"] for value in uid_to_player_map.values()]
    print(f"\n\nThe existing player IDs are {existing_player_ids}\n\n")
    next_id = game_manager.get_next_player_id(existing_player_ids)

    uid_to_player_map[player_uid] = {"player_name": player_name, "player_id": next_id}
    print(f"\n\nUID to player map created {uid_to_player_map}\n\n")
    #session["uids"] = uid_to_player_map

    # TODO - this is repetition with get_player_list but can't seem to call that func
    #emit("update player list", json.dumps(session.get("uids")), broadcast=True)
    emit("update player list", json.dumps(uid_to_player_map), broadcast=True)
    flash_io(f"You've joined the game with name {player_name} and player ID {next_id}")


@socketio.on('stand_up')
def on_stand_up():
    global uid_to_player_map
    #uid_to_player_map = session.get("uids")
    # TODO - add in cookie to track users. Currently refreshing page results in a new SID/users
    player_uid = request.cookies.get("player_uid")

    # uid_to_player_map = session.get("uids")

    flash_io(
        f'Player id {uid_to_player_map[player_uid]["player_id"]} with {uid_to_player_map[player_uid]["player_name"]} has left the game.')
    del uid_to_player_map[player_uid]
    #session["uids"] = uid_to_player_map

    #emit("update player list", json.dumps(session.get("uids")), broadcast=True)
    emit("update player list", json.dumps(uid_to_player_map), broadcast=True)

# @socketio.on("get hand")
# def get_hand():
#     global uid_to_player_map
#
#     player_hands = {}
#     for p in game_manager.scorer.players:
#         player_name = p.name
#         player_hands[player_name] = p.get_player_card_names()
#
#     player_uid = request.cookies.get("player_uid")
#     player_name = uid_to_player_map[player_uid]["player_id"]
#     socketio.emit("update hand", json.dumps(player_hands[player_name]), to=request.sid)


# @socketio.on("get current player")
# def get_current_player():
#     print("\nResponding to get player request")
#     player_uid = request.cookies.get("player_uid")
#     is_cur_player = is_current_player(player_uid)
#     game_status = {"game_phase": game_manager.game_phase.value, "is_current_player": is_cur_player}
#     print(f"\nGame status {game_status}")
#     emit("update game phase", json.dumps(game_status), broadcast=True)

# @socketio.on("get game phase")
# def call_get_game_phase():
#     emit_game_phase(request)


@socketio.on("choose card to play")
def choose_card_to_play(card_to_play):
    print(f"\n\nI am setting the card to play to {card_to_play}\n\n")
    game_manager.selected_card_to_play = card_to_play
    game_manager.game_phase = GameState.CHOOSE_WHERE_TO_PLAY
    emit_board_state(request)
    # emit_game_phase(request)
    # emit("update game phase", json.dumps(game_manager.game_phase.value))


@socketio.on("draw card")
def draw_card():
    global uid_to_player_map
    #uid_to_player_map = session.get("uids")
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]["player_id"]
    player_to_draw = game_manager.scorer.get_player_instance(player_name)
    player_to_draw.draw_card_from_deck()

    game_manager.num_cards_drawn_current_turn += 1
    if game_manager.num_cards_drawn_current_turn >= 2:
        game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    # Sends the updated player hand and board state to all players
    get_board_state(request)


@socketio.on("discard card")
def discard_card(card_to_discard):
    print(f"\n\nDiscarding a card: {card_to_discard}")
    game_manager.current_player.discard_card(card_to_discard, to_discard=True)

    is_game_over = game_manager.check_if_game_is_over()

    if is_game_over:
        game_manager.game_phase = GameState.SCORING
        return redirect(url_for("game_over"))

    game_manager.start_next_round()

    emit_board_state(request)


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

    #global uid_to_player_map
    #num_players = len(session.get("uids").keys())
    #num_players = len(uid_to_player_map.keys())
    #game_manager.num_players = num_players
    #game_manager.setup_scorer()
    #print(f"\n\nThe amount of players in the game is {len(game_manager.scorer.players)}!\n\n")

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


# @app.route("/draw_card_from_deck_old", methods=["POST"])
# def draw_card_from_deck_old():
#     """
#     Draws a card from the deck and adds it to the players hand. Progresses to the next phase (i.e. play card)
#     when two cards have been drawn
#     # TODO - if multiplayer is implemented, check will be needed that correct player tries to perform an action
#     """
#     if game_manager.current_player.deck.get_amt_of_cards_left() <= 0:
#         flash("The deck is empty. Scoring will start after the current turn is complete.", "error")
#         return redirect(url_for("main"))
#
#     game_manager.current_player.draw_card_from_deck()
#     game_manager.num_cards_drawn_current_turn += 1
#     if game_manager.num_cards_drawn_current_turn >= 2:
#         game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY
#
#     return redirect(url_for("main"))


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
    print(f"\nYou are trying to play {card_to_play}\n\n")
    row = int(request.form["coords"][0])
    column = int(request.form["coords"][1])
    # row, column = eval(request.form["coords"])
    # row, column = int(row), int(column)

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





# @app.route("/discard_card_old", methods=["POST"])
# def discard_card_old():
#     """
#     Discards a chosen card from the player's hand. Then checks if the game is over (i.e. deck is empty).
#     If it is, navigate to the scoring screen. If it's not, start the next player's turn.
#     """
#     card_to_discard = request.form["card_name"]
#     game_manager.current_player.discard_card(card_to_discard, to_discard=True)
#
#     game_over_bool = game_manager.check_if_game_is_over()
#
#     if game_over_bool:
#         game_manager.game_phase = GameState.SCORING
#         return redirect(url_for("game_over"))
#
#     game_manager.start_next_round()
#
#     emit_board_state(request)
#
#     # socketio.emit("update game phase", json.dumps(game_manager.game_phase.value), broadcast=True)
#
#     return redirect(url_for("main"))


# @app.route("/choose_card_to_play_old", methods=["POST"])
# def choose_card_to_play_old():
#     """
#     Identifies the card the player has chosen to play and sets the game manager to remember the card. Then progresses
#     the game state so the player can choose where to place the selected card
#     """
#     selected_card_to_play = request.form['card_name']
#     game_manager.selected_card_to_play = selected_card_to_play
#     game_manager.game_phase = GameState.CHOOSE_WHERE_TO_PLAY
#     return redirect(url_for("main"))


if __name__ == "__main__":
    socketio.run(app)
    # app.run(host="0.0.0.0")

# def emit_game_phase(r):
#     print("\nResponding to get phase request")
#     player_uid = r.cookies.get("player_uid")
#     print(f"\nUID: {player_uid}")
#     is_cur_player = is_current_player(player_uid)
#     game_status = {"game_phase": game_manager.game_phase.value, "is_current_player": is_cur_player}
#     print(f"\nGame status {game_status}")
#     socketio.emit("update game phase", json.dumps(game_status), broadcast=True)
