# Board config
BOARD_ROWS = 6
BOARD_COLUMNS = 10

# Card configs
TREES = ["Cassia", "Blue Spruce", "Jacaranda", "Oak", "Royal Poinciana", "Tulip Popular", "Dogwood", "Cherry Blossom"]
CARDS_PER_TREE_TYPE = 8
NUM_CARDS_STARTING_HAND = 7

# Overall configs
NUM_PLAYERS = 2

# Shows amount of tree types based on amount of players: num_players : num trees
# The option of having 1 player is to enable easy testing
# TODO - to support four players, add 10 tree types (currently only 8 exists)
AMT_TREES_PER_AMT_PLAYER = {
    1: 3,
    2: 6,
    3: 8,
}