from player_lv_V1 import PlayerLV1
# from player_lv_V2 import PlayerLV2
from player_lv_V3 import PlayerLV3
from game.board import Board
from game.player import Player
from game.cli import Game
                
if __name__ == "__main__":
    lv1_black = PlayerLV1(2, "Black")
    lv1_white = PlayerLV1(2, "White")
    lv2_black = PlayerLV2(1, "Black")
    lv2_white = PlayerLV2(1, "White")
    lv3_black = PlayerLV3(1, "Black")
    lv3_white = PlayerLV3(1, "White")
    player_black = Player(1, "Black")
    player_white = Player(2, "White")

    # Can choose different modes
    # game = Game(Board(15, 15), lv1_black, lv2_white)
    game = Game(Board(15, 15), lv2_black, lv1_white)
    # game = Game(Board(15, 15), lv2_black, player_white)
    # game = Game(Board(15, 15), player_black, lv2_white)

    game.play_one_round()
