from flask import Flask, render_template, request
from logic import game_logic

# Flask config
app = Flask(__name__)
app.config['DEBUG'] = False

card_to_play = None


@app.route("/draw_card_from_deck", methods=["POST"])
def draw_card_from_deck():
    game_logic.scorer.players[0].draw_card_from_deck()

    return main()


@app.route("/choose_coordinates", methods=["POST"])
def choose_coordinates():
    """
    Gets form input from the tile selected by the user in the format row, column (e.g. 1,1)
    """
    global card_to_play
    row, column = eval(request.form["coords"])

    print("\n\n\n")
    print(row)
    print(column)
    print("\n\n\n")
    row, column = int(row), int(column)
    # TODO - refactor so players[0] references the player that clicked the button
    game_logic.scorer.players[0].play_card(card_to_play, row=row, column=column)
    card_to_play = None
    game_logic.game_phase = "Choose Card"

    return main()

@app.route("/play_card", methods=["POST"])
def play_card():
    global card_to_play
    # Verify that the game state is playing a card!
    # if not game_logic.current_game_state == "Draw"
        # raise ValueError("It's not time to draw"
    # If not request.form.player == game_logic.current_player:
        # raise ValueError("It's not your time to play!")
    # Check who the player is
    #player_name = request.form.player
    card_played = request.form['card_name']
    #rand_row = random.randrange(0,6)
    #rand_col = random.randrange(0,10)

    card_to_play = card_played

    # print("\n\n\n")
    # print(card_played)
    # print("See card above")
    # print("\n\n\n")

    #row = 5
    #column = 5

    game_logic.game_phase = "Choose Coordinates"

    return main()


@app.route("/", methods=["GET"])
def main():

    player_hand = game_logic.scorer.players[0].get_player_card_names()
    player_hands = {"Player 1": player_hand}

    player_board = game_logic.scorer.players[0].board.board_grid
    player_boards = {"Player 1": player_board}

    #current_players_turn = game_logic.current_player
    #current_game_phase = game_logic.current_game_phase

    game_phase = game_logic.game_phase

    return render_template(
        'main.html',
        player_hands=player_hands,
        player_boards=player_boards,
        game_phase=game_phase,
    )


if __name__ == "__main__":
    app.run(debug=True)

# Next steps
# Implement drawing from the deck?
# Implementing more board states, e.g. Draw -> Choose Card -> Choose Coords

# What to pass to the template?
# Player hands - {"Player 1": ["Oak 1", "Oak 2", "Oak 3]}
# Current Player taking an action - e.g. "Player 1"
# Game States -> Choose Draw, Choose Discard, Choose Play Card, Choose Play Coordinates
# Board State
# Graveyard

# What does the template pass back?
# Actions (i.e.: Draw from graveyard, draw from deck, play card X, discard card Y)
# Who took the action
# Example data passed back (initial version) ("1", "draw graveyard 1")
# Long-term the UI should call different functions, not a single one


# Thoughts?
# Weakness in always sending all cards and re-rendering? Might make hand re-render on every action
# Should I pass the entire player class? Or board class? Probably not. Just need a JSON format of needed data. Decouple UI and backend.
# We should check if the