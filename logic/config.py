# Board config
BOARD_ROWS = 6
BOARD_COLUMNS = 10
EMPTY_SLOT_DISPLAY_SHORTHAND = "  "
BOARD_SLOT_DIVIDER = "|"

# Deck configs
# TODO - add in these trees to use when more than 2 players: ["Lilac", "Magnolia", "Maple", "Olive"]
TREES = ["Cassia", "Dogwood", "Jacaranda", "Oak"]
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