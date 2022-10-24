import json
from logic import game_creator, GameState, GameManager
import random
from flask import Flask, render_template, request, url_for, make_response
from flask_socketio import SocketIO, emit

# Flask config
app = Flask(__name__)
app.secret_key = b'this-is-a-dev-env-secret-key-abc-abc'
app.debug = True
#app.config['SESSION_TYPE'] = "filesystem"
socketio = SocketIO(app) # logger=True, manage_session=False
# app.host="0.0.0.0"

# Global variables
uid_to_player_map = {}
game_manager = GameManager


### LOBBY VIEWS ###


@app.route("/lobby", methods=["GET"])
def lobby():
    response = make_response(render_template("lobby.html"))
    player_uid = request.cookies.get("player_uid")

    if player_uid:
        # Don't set a new cookie if a uid cookie exists
        return response

    # Otherwise, create a new user ID (uid) and set it in a cookie
    # TODO - create a MD5 hash or something instead to remove risk of collision
    response.set_cookie("player_uid", value=str(random.randrange(1, 999)))
    return response


@socketio.on('sit down')
def on_sit_down(player_name):
    global uid_to_player_map
    global game_manager

    if player_name in uid_to_player_map.values():
        raise ValueError(f"{player_name} already exists. Please choose another name")

    # TODO - check if cookie exists - otherwuse redirect to lobby?
    player_uid = request.cookies.get("player_uid")

    # existing_player_ids = [value["player_id"] for value in uid_to_player_map.values()]
    # print(f"\n\nThe existing player IDs are {existing_player_ids}\n\n")
    # next_id = game_manager.get_next_player_id(existing_player_ids)

    # TODO - does it make sense to add each player in two places? Or should
    # the player be added to the UID mapping and then created later?
    #game_creator.add_player(player_name)
    # uid_to_player_map[player_uid] = {"player_name": player_name, "player_id": next_id}
    uid_to_player_map[player_uid] = player_name
    # print(f"\n\nUID to player map created {uid_to_player_map}\n\n")

    emit("update player list", json.dumps(list(uid_to_player_map.values())), broadcast=True)
    flash_io(f"You've joined the game as {player_name}")


@socketio.on('stand up')
def on_stand_up():
    global uid_to_player_map
    player_uid = request.cookies.get("player_uid")

    flash_io(f"Player {uid_to_player_map[player_uid]} has left the game.")
    # game_creator.remove_player(uid_to_player_map[player_uid])
    del uid_to_player_map[player_uid]

    emit("update player list", json.dumps(list(uid_to_player_map.values())), broadcast=True)


@socketio.on("start game")
def get_board_state():
    global uid_to_player_map
    global game_manager

    player_names = list(uid_to_player_map.values())

    if len(player_names) < 1:
        flash_io("Not enough players connected. Add more players.", "warning")
    else:
        game_manager = game_creator.create_game(player_names)
        emit('redirect', json.dumps(url_for('main')), broadcast=True)


@socketio.on("get player list")
def get_player_list():
    global uid_to_player_map
    emit("update player list", json.dumps(uid_to_player_map), broadcast=True)


#### MAIN LOGIC ###

def flash_io(text: str, category: str = "dark") -> None:
    """Send "message" to the client with the given error category"""
    emit('message', json.dumps({"text": text, "category": category}))


def emit_game_state(req) -> (dict, list[str]):
    global uid_to_player_map
    global game_manager

    player_uid = req.cookies.get("player_uid")

    # Get the player's hand
    player_name = uid_to_player_map[player_uid]
    print(f"I will try to find the instance of {player_name}")
    player_instance = game_manager.get_player_instance(player_name)
    cards_on_hand = player_instance.get_player_card_names()

    # Does a reverse loopup to find the uid (key) based on the current player's player name (value)
    # current_player_uid = list(uid_to_player_map.keys())[list(uid_to_player_map.values()).index(current_player_name)]
    # print([item for item in uid_to_player_map.items() if item[0] == "Apple"])

    # Get the UID and player name for the current player
    current_player_name = game_manager.current_player.name
    # TODO - refactor list comprehension here is odd
    current_player_id = [{"uid": item[0], "player_name": item[1]} for item in uid_to_player_map.items() if item[1] == current_player_name][0]

    # for uid in uid_to_player_map:
    #     if uid_to_player_map[uid] == current_player_name:
    #         uid_name_mapping = {"uid": uid, "player_name": uid_to_player_map[uid]["player_name"]}
    #         print(f"The current name is {uid_to_player_map[uid]} which means UID {uid}")

    # Get the current game phase (e.g. draw, choose card to play)
    game_phase = game_manager.game_phase.value

    # Get the remaining amount of cards in the deck
    num_cards_in_deck = game_manager.get_amt_of_cards_left()

    # Get top discard cards
    top_discard_cards = {}
    # TODO - refactor
    for p in game_manager.scorer.players:
        top_discard_cards[p.name] = p.discard.get_top_card(only_str=True)

    # Get the board for all players
    player_boards = {}
    # TODO - to think about: where is the source of truth of what players exist? GameManager?
    for uid in uid_to_player_map:
        p_instance = game_manager.get_player_instance(uid_to_player_map[uid])
        player_boards[uid] = p_instance.board.get_board_state()

    # Construct the game state dict
    board_state_dict = {"game_phase": game_phase,
                        "current_player_id": current_player_id,
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


@socketio.on("choose card to play")
def choose_card_to_play(card_to_play):
    global game_manager
    print(f"\n\nI am setting the card to play to {card_to_play}\n\n")
    game_manager.select_card_to_play(card_to_play)
    #selected_card_to_play = card_to_play
    #game_manager.game_phase = GameState.CHOOSE_WHERE_TO_PLAY
    emit_game_state(request)


@socketio.on("draw card")
def draw_card_from_deck():
    global uid_to_player_map
    global game_manager
    
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]
    game_manager.draw_card(player_name)

    # player_to_draw = game_manager.get_player_instance(player_name)
    # player_to_draw.draw_card_from_deck()
    # game_manager.num_cards_drawn_current_turn += 1
    # if game_manager.num_cards_drawn_current_turn >= 2:
    #     game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    # TODO - Can emit state be set to run after each request, or at least for some?
    # Maybe we can have a custom decorator for that that calls emit_game_state at the end
    emit_game_state(request)


@socketio.on("discard card")
def discard_card(card_to_discard):
    global game_manager

    # TODO - the lines to get the player name are a bit repetitive - break out into func=
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]

    game_manager.discard_card(player_name=player_name, card_to_discard=card_to_discard)

    # print(f"\n\nDiscarding a card: {card_to_discard}")
    # game_manager.current_player.discard_card(card_to_discard, to_discard=True)

    #is_game_over = game_manager.is_game_over()
    # if is_game_over:
    #     game_manager.game_phase = GameState.SCORING
    #     emit('end game', json.dumps(url_for('game_over')), broadcast=True)

    if game_manager.game_phase == GameState.SCORING:
        # The deck is empty, meaning that the game is over - redirecting to game over/scoring screen
        emit('end game', json.dumps(url_for('game_over')), broadcast=True)

    #game_manager.start_next_round()
    emit_game_state(request)


@socketio.on("draw from discard")
def draw_from_discard(player_to_draw_from):
    global game_manager
    print(f"I am drawing from discard from {player_to_draw_from}")
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]
    #player_instance = game_manager.get_player_instance(player_to_draw_from)

    try:
        #game_manager.current_player.draw_card_from_discard(player_to_draw_from=player_instance)
        game_manager.draw_card(player_name=player_name, to_draw_from=player_to_draw_from)
    except ValueError as e:
        # User drew from empty discard or some other error occurred
        flash_io(str(e), "warning")

    # game_manager.num_cards_drawn_current_turn += 1
    # if game_manager.num_cards_drawn_current_turn >= 2:
    #     game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY

    emit_game_state(request)


@socketio.on("choose coords")
def choose_coords(chosen_coords):
    global game_manager
    print(f"\n\nCommencing choose coords with {chosen_coords}\n\n")

    card_to_play = game_manager.selected_card_to_play
    row = int(chosen_coords[0])
    column = int(chosen_coords[1])
    print(f"\nYou are trying to play {card_to_play} at ({row},{column})")

    # TODO - is it better to always read the cookie value, or should we just reference current player?
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]

    try:
        game_manager.play_card_at_chosen_coords(player_name=player_name, row=row, column=column)
    except ValueError as e:
        # User chose an invalid location for a card (e.g. not adjacent to an existing card)
        # - notifying user and resetting to start of play phase
        # game_manager.selected_card_to_play = None
        # game_manager.game_phase = GameState.CHOOSE_CARD_TO_PLAY
        flash_io(str(e) + " Please re-select what card to play", "warning")
    emit_game_state(request)


@app.route("/game", methods=["GET"])
def main():
    return render_template("game.html")


@app.route("/game_over", methods=["GET"])
def game_over():
    """
    Gets the data to display in the UI on the game over screen and then renders the page
    """
    # TODO - this is repetition with main() - break out into function?
    global game_manager
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
                player_instance = game_manager.get_player_instance(player)
                (row, col) = player_instance.board.find_coords_of_card(card)
                # If is player num, row, col (e.g. 111 is Player 1 row 1 column 1)
                coords_id = str(player)[-1] + str(row) + str(col)
                list_of_coords.append(coords_id)
            top_paths[player][tree_dict]["Path"] = list_of_coords

    return render_template("game_over.html",
                           player_hands=player_hands,
                           player_boards=player_boards,
                           top_paths=top_paths,
                           winners=winners
                           )


if __name__ == "__main__":
    socketio.run(app)

