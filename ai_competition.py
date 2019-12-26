from dummy_ai import DummyAI
from Player_lv import Playerlv
from gomoku import PlayerLV, MoveTree
from classes import *
                
if __name__ == "__main__":
    Player_lv1 = Playerlv(1, "Black")
    Player_lv2 = Playerlv(2, "White")
    Player_LV1 = PlayerLV(1, "Black")
    Player_LV2 = PlayerLV(2, "White")
    Player_black = Player(1, "Black")
    Player_white = Player(2, "White")

    # Can choose different modes
    # game = Game(Board(15, 15), Player_lv1, Player_LV2)
    # game = Game(Board(15, 15), Player_black, Player_LV2)
    game = Game(Board(15, 15), Player_LV1, Player_white)

    # Not used currently
    # Player_zf = DummyAI(2, 1, "White")
    # game = Game(Board(15, 15), Player_lv1, Player_zf)
    # game = Game(Board(15, 15), Player_zf, Player_lv2)
    # game = Game(Board(15, 15), Player_black, Player_zf)
    # game = Game(Board(15, 15), Player_zf, Player_white)

    game.play_one_round()
