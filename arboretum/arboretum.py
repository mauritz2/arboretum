import json
from game import game_creator, GameState, GameManager
import random
from flask import Flask, render_template, request, url_for, make_response
from flask_socketio import SocketIO, emit

"""
Purpose of arboretum.py: 
- Lets players join the game
- Creates the game when the players are ready
- Get player game input from the client
- Use the game_manager to execute player actions
- Send updated board states to the client  
- Handle errors from the game library to make sure game doesn't crash due to any invalid actions

It does not
- Do game logic (e.g. keep track of who's turn it is, change game phase). That is managed by the game_manager.
- Throw errors when players do the wrong thing, e.g. play when it's not their turn. It's trying to not crash the game.
- Communicate with all the classes in the game module (only game creator and game manager)

TODO:
Shorter-term
- Alignment CSS fine tuning
- Dynamic header showing what game phase the current player is at
- Fix CSS bug where other cards display on top of zoomed card
- Refactor JS code
- Update path highlighting now that coords have changed
- Fix buttons and overlays so they match card size
- Better game-over screen where you can click to display board-cards of that player
- Implement logic to make cards amounts dynamic based on player amount
- Fix failing game logic test cases

Longer-term
- Light only up possible card placements (i.e. adjacent to existing trees)
- Make design more responsive so it fits on smaller screens

"""

# Flask config
app = Flask(__name__)
app.secret_key = b'this-is-a-dev-env-secret-key-abc-abc'
app.debug = True
socketio = SocketIO(app)
# app.host="0.0.0.0"

# Global variables
uid_to_player_map = {}
game_manager = GameManager


### LOBBY VIEWS ###


@app.route("/", methods=["GET"])
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
        flash_io(f"{player_name} already exists. Please choose another name", "warning")
        return

    if len(player_name) == 0:
        # TODO - client-side validation would be better here
        flash_io("Player name can't be blank. Please choose a name and join the game.", "warning")
        return

    player_uid = request.cookies.get("player_uid")
    uid_to_player_map[player_uid] = player_name
    # TODO - create special func for updating the player list
    emit("update player list", json.dumps(list(uid_to_player_map.values())), broadcast=True)
    flash_io(f"You've joined the game as {player_name}")


@socketio.on('stand up')
def on_stand_up():
    global uid_to_player_map
    player_uid = request.cookies.get("player_uid")

    if player_uid not in uid_to_player_map:
        flash_io(f"Can't leave - you haven't joined the game", "warning")
        return

    flash_io(f"You have left the game")
    del uid_to_player_map[player_uid]

    emit("update player list", json.dumps(list(uid_to_player_map.values())), broadcast=True)


@socketio.on("start game")
def get_board_state():
    global uid_to_player_map
    global game_manager

    player_names = list(uid_to_player_map.values())

    if len(player_names) < 1:
        flash_io("At least one player needs to be connected to play. Add more players and then start the game.", "warning")
        return

    game_manager = game_creator.create_game(player_names)
    emit('redirect', json.dumps(url_for('main')), broadcast=True)


@socketio.on("get player list")
def get_player_list():
    global uid_to_player_map
    emit("update player list", json.dumps(list(uid_to_player_map.values())), broadcast=True)


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
    player_instance = game_manager.get_player_instance(player_name)
    cards_on_hand = player_instance.get_player_card_names()

    # Get the UID and player name for the current player
    current_player_name = game_manager.current_player.name
    # TODO - refactor list comprehension here is odd
    # current_player_uid = list(uid_to_player_map.keys())[list(uid_to_player_map.values()).index(current_player_name)]
    current_player_id = [{"uid": item[0], "player_name": item[1]} for item in uid_to_player_map.items() if item[1] == current_player_name][0]

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
    # TODO - can we send the player name here as well? Or can we send a mapping between UID and player separately?
    # Currently no way to show the names of each players side board
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
    # TODO - remove this? Not sure if needed, maybe emit game stat can be socketio.on()
    if req:
        emit_game_state(req)
    else:
        emit_game_state(request)


@socketio.on("choose card to play")
def choose_card_to_play(card_to_play):
    global game_manager
    game_manager.select_card_to_play(card_to_play)
    emit_game_state(request)


@socketio.on("draw card")
def draw_card_from_deck():
    global uid_to_player_map
    global game_manager
    
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]

    if player_name != game_manager.current_player.name:
        flash_io(f"It's not your turn to draw a card. Current player's turn is {game_manager.current_player.name}")
        return

    game_manager.draw_card(player_name)

    # TODO - Can emit state be set to run after each request, or at least for some?
    # Maybe we can have a custom decorator for that that calls emit_game_state at the end
    emit_game_state(request)


@socketio.on("discard card")
def discard_card(card_to_discard):
    global game_manager

    # TODO - the lines to get the player name are a bit repetitive - break out into func=
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]

    if player_name != game_manager.current_player.name:
        flash_io(f"It's not your turn to discard. Current player's turn is {game_manager.current_player.name}", "warning")
        return
    else:
        game_manager.discard_card(player_name=player_name, card_to_discard=card_to_discard)

        print(f"The current game state is {game_manager.game_phase}\n")
        if game_manager.game_phase == GameState.SCORING:
            print("Going to redirect\n")
            # The deck is empty, meaning that the game is over - redirecting to game over/scoring screen
            emit('redirect', json.dumps(url_for('game_over')), broadcast=True)

        emit_game_state(request)


@socketio.on("draw from discard")
def draw_from_discard(player_to_draw_from):
    global game_manager
    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]

    if player_name != game_manager.current_player.name:
        flash_io(f"It's not your turn to discard. Current player's turn is {game_manager.current_player.name}", "warning")
        return

    try:
        game_manager.draw_card(player_name=player_name, to_draw_from=player_to_draw_from)
    except ValueError as e:
        # User drew from empty discard or some other error occurred
        flash_io(str(e), "warning")

    emit_game_state(request)


@socketio.on("choose coords")
def choose_coords(chosen_coords):
    global game_manager
    print(f"\n\nCommencing choose coords with {chosen_coords}\n\n")

    player_uid = request.cookies.get("player_uid")
    player_name = uid_to_player_map[player_uid]

    if player_name != game_manager.current_player.name:
        flash_io(f"It's not your turn to choose where to place a card. Current player's turn is {game_manager.current_player.name}")
        return

    row = int(chosen_coords[0])
    column = int(chosen_coords[1])

    try:
        game_manager.play_card_at_chosen_coords(player_name=player_name, row=row, column=column)
    except ValueError as e:
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

