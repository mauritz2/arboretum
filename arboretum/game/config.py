# Board config
BOARD_ROWS = 6
BOARD_COLUMNS = 10

# Card configs
# TODO - dynamically increase the amount of cards based on amount of players
TREES = ["Cherry Blossom", "Tulip Popular", "Royal Poinciana", "Cassia", "Blue Spruce", "Jacaranda", "Oak"]
CARDS_PER_TREE_TYPE = 8
NUM_CARDS_STARTING_HAND = 7

# Overall configs
# TODO - make sure that game works with more than 2 players
NUM_PLAYERS = 2

# Shows amount of tree types based on amount of players: num_players : num trees
# The option of having 1 player is to enable easy testing
# AMT_TREES_PER_AMT_PLAYER = {
#     1: 6,
#     2: 6,
#     3: 8,
#     4: 10
# }


# TODO - update to real values above when I have more cards
AMT_TREES_PER_AMT_PLAYER = {
    1: 3,
    2: 3,
    3: 4,
}