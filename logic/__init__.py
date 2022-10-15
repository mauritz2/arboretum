from logic.player import Player
from logic.board import Board
from logic.deck import Deck
from logic.scorer import Scorer
from logic.card import Card
from logic.discard import Discard
from logic.gamemanager import GameManager
from logic.gamemanager import GameState, player_game_state_messages
import logic.config as config

game_manager = GameManager(config.NUM_PLAYERS)

# TODO - removing data below used in troubleshooting
# # Player 1 paths
oak2 = Card(tree_type="Oak", tree_val=2)
cas4 = Card(tree_type="Cassia", tree_val=4)
jac6 = Card(tree_type="Jacaranda", tree_val=6)
oak7 = Card(tree_type="Oak", tree_val=7)

game_manager.scorer.players[0].board.board_grid[2][2] = oak2
game_manager.scorer.players[0].board.board_grid[2][3] = cas4
game_manager.scorer.players[0].board.board_grid[2][4] = jac6
game_manager.scorer.players[0].board.board_grid[2][5] = oak7

blue1 = Card(tree_type="Blue Spruce", tree_val=1)
blue2 = Card(tree_type="Blue Spruce", tree_val=2)
blue3 = Card(tree_type="Blue Spruce", tree_val=3)
blue4 = Card(tree_type="Blue Spruce", tree_val=4)

game_manager.scorer.players[0].board.board_grid[3][2] = blue1
game_manager.scorer.players[0].board.board_grid[3][3] = blue2
game_manager.scorer.players[0].board.board_grid[3][4] = blue3
game_manager.scorer.players[0].board.board_grid[3][5] = blue4

blue8 = Card(tree_type="Blue Spruce", tree_val=8)

game_manager.scorer.players[0].board.board_grid[1][5] = blue8

# Player 2 paths
jac1 = Card(tree_type="Jacaranda", tree_val=1)
jac2 = Card(tree_type="Jacaranda", tree_val=2)
jac3 = Card(tree_type="Jacaranda", tree_val=3)
jac4 = Card(tree_type="Jacaranda", tree_val=4)

game_manager.scorer.players[1].board.board_grid[3][2] = jac1
game_manager.scorer.players[1].board.board_grid[3][3] = jac2
game_manager.scorer.players[1].board.board_grid[3][4] = jac3
game_manager.scorer.players[1].board.board_grid[3][5] = jac4

game_manager.scorer.players[1].board.board_grid[5][2] = blue1
game_manager.scorer.players[1].board.board_grid[5][3] = blue2
game_manager.scorer.players[1].board.board_grid[5][4] = blue3
game_manager.scorer.players[1].board.board_grid[5][5] = blue4
