from flask import Flask, render_template, request
from logic import game_logic
from logic import config

# Flask config
app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/play_card", methods=["POST"])
def play_card():
    # Verify that the game state is playing a card!
    # if not game_logic.current_game_state == "Draw"
        # raise ValueError("It's not time to draw"
    # If not request.form.player == game_logic.current_player:
        # raise ValueError("It's not your time to play!")
    # Check who the player is
    #player_name = request.form.player
    #card_played = request.form.card_played
    #row = 5
    #column = 5

    game_logic.scorer.players[0].place_tree(card_name="Oak 1", row=5, column=5)
    main()

@app.route("/", methods=["GET"])
def main():

    player_hand = game_logic.scorer.players[0].get_player_card_names()
    player_hands = {"Player 1": player_hand}

    player_board = game_logic.scorer.players[0].board.board_grid
    player_boards = {"Player 1": player_board}

    current_players_turn = game_logic.current_player
    current_game_phase = game_logic.current_game_phase

    current_game_phase = "Draw"
    current_players_turn = "Player 1"

    return render_template(
        'main.html',
        player_hands=player_hands,
        player_boards=player_boards,
        current_game_phase=current_game_phase)

if __name__ == "__main__":
    app.run(debug=True)

# Next steps
# Render two players cards
# Switch art to Arboretum cards
# Do if-statement breakdown of all actions - then break out so UI calls separate funcs

# What to pass to the template?
# Player hands - {"Player 1": ["Oak 1", "Oak 2", "Oak 3]}
# Current Player taking an action - e.g. "Player 1"
# Game States -> Choose Draw, Choose Discard, Choose Play Card, Choose Play Coordinates
# Board State



# What does the template pass back?
# Actions (i.e.: Draw from graveyard, draw from deck, play card X, discard card Y)
# Who took the action
# Example data passed back (initial version) ("1", "draw graveyard 1")
# Long-term the UI should call different functions, not a single one


# Thoughts?
# Weakness in always sending all cards and re-rendering? Might make hand re-render on every action
# Should I pass the entire player class? Or board class? Probably not. Just need a JSON format of needed data. Decouple UI and backend.
# We should check if the