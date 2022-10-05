from flask import Flask, render_template
from logic import my_game


# Flask config
app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def play_game():
    player_hand = my_game.scorer.players[0].get_player_card_names()
    player_hands = {"Player 1": player_hand}

    return render_template(
        'main.html',
        player_hands=player_hands)

if __name__ == "__main__":
    app.run(debug=True)

# Milestones
# Render a 10x10 board grid


# Render two players cards
# Switch art to Arboretum cards
# Do if-statement breakdown of all actions - then break out so UI calls separate funcs

# What to pass to the template?
# Player hands - {"Player 1": ["Oak 1", "Oak 2", "Oak 3]}
# Current Player taking an action - e.g. "Player 1"
# Game State (e.g. "Draw", "Discard", "Play")
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