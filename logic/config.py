# Board config
BOARD_ROWS = 6
BOARD_COLUMNS = 10
EMPTY_SLOT_DISPLAY_SHORTHAND = "  "
BOARD_SLOT_DIVIDER = "|"

# Deck configs
# All: ["Cassia", "Blue Spruce", "Jacaranda", "Olive", "Lilac", "Magnolia", "Maple", "Royal Poinciana", "Oak", Willow"]
# The online rules don't seem to include Blue Spruce for some reason, but it's for sure in the game
TREES = ["Cassia", "Blue Spruce", "Jacaranda", "Oak"]
CARDS_PER_TREE_TYPE = 8
NUM_CARDS_STARTING_HAND = 7

# Overall configs
# TODO - make sure that game works with more than 2 players
NUM_PLAYERS = 2

# Generate a unique board representation of each card
CARD_SHORTHANDS = {}
for tree in TREES:
	for i in range(1, CARDS_PER_TREE_TYPE+1):
		CARD_SHORTHANDS[f"{tree} {i}"] = f"{tree[0]}{i}"

# Cassia second path is highlighted!!