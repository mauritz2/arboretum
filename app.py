#import random
#from copy import deepcopy
from flask import Flask, render_template #session, request,
#from collections import defaultdict
app = Flask(__name__)
app.config['DEBUG'] = True
#players = defaultdict(dict)
#first_player = None
#player_current_cards = defaultdict(dict)
#player_current_cards['0'] = {}
#player_current_cards['1'] = {}
#player_current_cards['2'] = {}
#player_current_cards['3'] = {}
#current_type = None
#comp_players_left = ['0', '1', '2']
#types = ['spades', 'clubs', 'diamonds', 'hearts']
#players_score = {}
#players_score['0'] = 0
#players_score['1'] = 0
#players_score['2'] = 0
#players_score['3'] = 0
#log_message = None
#winner_player = None

# def flush_for_new_hand():
#     global player_current_cards
#     global current_type
#     global log_message
#
#     player_current_cards = defaultdict(dict)
#     player_current_cards['0'] = {}
#     player_current_cards['1'] = {}
#     player_current_cards['2'] = {}
#     player_current_cards['3'] = {}
#     current_type = None
#     log_message = None


# def get_from_list_in_range(start, end, alist):
#     result = []
#     for item in alist:
#         if item <= end and item >= start:
#             if item % 13 != 0:
#                 result.append(item % 13)
#             else:
#                 result.append(13)
#     return result
#
#
# def start_game():
#     big_set = range(1, 53)
#     for i in range(4):
#         player_set = random.sample(big_set, 13)
#         for value in player_set:
#             big_set.remove(value)
#         players[str(i)]['spades'] = get_from_list_in_range(1, 13, player_set)
#         players[str(i)]['clubs'] = get_from_list_in_range(14, 26, player_set)
#         players[str(i)]['diamonds'] = get_from_list_in_range(27, 39, player_set)
#         players[str(i)]['hearts'] = get_from_list_in_range(40, 52, player_set)
#         # import pdb; pdb.set_trace()
#         if 2 in players[str(i)]['clubs']:
#             global first_player
#             first_player = str(i)
#
# def find_min_value(alist):
#     temp_list = deepcopy(alist)
#     if 1 in alist:
#         temp_list.remove(1)
#         temp_list.append(14)
#     min_value = min(temp_list)
#     if min_value == 14:
#         min_value = 1
#     return min_value
#
#
# def find_max_value(alist):
#     temp_list = deepcopy(alist)
#     if 1 in alist:
#         temp_list.remove(1)
#         temp_list.append(14)
#     max_value = max(temp_list)
#     if max_value == 14:
#         max_value = 1
#     return max_value
#
#
# def get_cards_to_play(start_player, current_type):
#     card_type = deepcopy(current_type)
#     player = deepcopy(start_player)
#     # import pdb; pdb.set_trace()
#     if player != '3' and 'card' not in player_current_cards[player]:
#         # import pdb; pdb.set_trace()
#         cards_choices = players[player][current_type]
#         if len(cards_choices) != 0:
#             player_card = find_min_value(cards_choices)
#         else:
#             remaining_types = deepcopy(types)
#             remaining_types.remove(card_type)
#             for tp in remaining_types:
#                 cards_choices = players[player][tp]
#                 if len(cards_choices) == 0:
#                     continue
#                 else:
#                     player_card = find_max_value(cards_choices)
#                     break
#             card_type = tp
#         player_current_cards[player]['type'] = card_type
#         # import pdb; pdb.set_trace()
#         player_current_cards[player]['card'] = player_card
#         players[player][card_type].remove(player_card)
#         next_player = str(int(player) + 1)
#         get_cards_to_play(next_player, current_type)
#
#
# def get_averages_of_cards(cards):
#     result = {}
#     for _type, values in cards.iteritems():
#         if len(values) == 0:
#             continue
#         elif 1 in values:
#             result[_type] = (sum(values) + 13)/float(len(values))
#         else:
#             result[_type] = sum(values)/float(len(values))
#     return result
#
#
# def get_current_type(player):
#     global players
#     cards_with_player = players[player]
#     cards_avg = get_averages_of_cards(cards_with_player)
#     values=list(cards_avg.values())
#     keys=list(cards_avg.keys())
#     card_type = keys[values.index(min(values))]
#     return card_type
#
#
# def validate(cardtype):
#     val = True
#     if len(players['3'][current_type]) == 0:
#         val = False
#     if cardtype != current_type and val:
#         return False
#     return True
#
# def has_clubs_two(card, cardtype):
#     global players
#     if 2 in players['3']['clubs'] and (card != 2 or cardtype != 'clubs'):
#         return True
#     return False
#
#
# def evaluate_cards():
#     global winner_player
#     global player_current_cards
#     valid_cards_mapping = {}
#     hearts_count = 0
#     for player, item in player_current_cards.iteritems():
#         if item['type'] == 'hearts':
#             hearts_count += 1
#         if item['type'] == current_type:
#             if item['card'] == 1:
#                 valid_cards_mapping[player] = 14
#             else:
#                 valid_cards_mapping[player] = item['card']
#     values=list(valid_cards_mapping.values())
#     keys=list(valid_cards_mapping.keys())
#     winner_player = keys[values.index(max(values))]
#     players_score[winner_player] += hearts_count
#
#     return winner_player
#
# def check_if_game_over():
#     global players
#     # import pdb; pdb.set_trace()
#     for _type, values in players['3'].iteritems():
#         if len(values) != 0:
#             return False
#     return True
#
@app.route("/", methods=['GET'])
def play_game():
    # data = None
    # global log_message
    # global current_type
    # global winner_player
    # global players_score
    # if hasattr(request, 'form'):
    #     data = request.form
    # # import pdb; pdb.set_trace()
    # if len(data.values()) == 0 or data is None:
    #     start_game()
    #     current_type = 'clubs'
    #     print players
    #     if first_player != '3':
    #         get_cards_to_play(first_player, current_type)
    # elif 'card' in data:
    #     # import pdb; pdb.set_trace()
    #     user_card = int(data['card'])
    #     user_card_type = data['type']
    #     if current_type is None:
    #         current_type = user_card_type
    #     if not validate(user_card_type):
    #         log_message = "Please choose card of %s" % current_type
    #     elif has_clubs_two(user_card, user_card_type):
    #         log_message = "Please play with clubs of 2"
    #     else:
    #         player_current_cards['3'] = {
    #             'type': user_card_type,
    #             'card': user_card
    #         }
    #         players['3'][user_card_type].remove(user_card)
    #         if first_player != '0':
    #             get_cards_to_play('0', current_type)
    #         evaluate_cards()
    #         log_message = "Player %s got this hand" % winner_player
    # elif not check_if_game_over():
    #     if 'is_hand_over' not in data:
    #         raise Exception("Unhandled condition")
    #     flush_for_new_hand()
    #     if winner_player != '3':
    #         current_type = get_current_type(winner_player)
    #         get_cards_to_play(winner_player, current_type)
    #     log_message = "It is your turn"
    # else:
    #     # import pdb; pdb.set_trace()
    #     values=list(players_score.values())
    #     keys=list(players_score.keys())
    #     game_winner = keys[values.index(min(values))]
    #     log_message = "Game over with winner %s" % game_winner
    #
    # print player_current_cards

    player_current_cards = {}
    log_message = None
    players = {'3':{}}
    players_score = None
    player_current_cards['0'] = {}
    player_current_cards['1'] = {}
    player_current_cards['2'] = {}
    player_current_cards['3'] = {}

    return render_template(
        'main.html',
        player_current_cards=player_current_cards,
        log_message=log_message,
        user_player=players['3'],
        players_score=players_score)


if __name__ == "__main__":
    app.run(debug=True)

# Milestones
# Render cards in the UI
# Render a players hand
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