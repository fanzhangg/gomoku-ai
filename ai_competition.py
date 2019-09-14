from dummy_ai import DummyAI
from Player_lv import Player_LV
from classes import *
                
if __name__ == "__main__":
    Player_lv = Player_LV(1, "Black")
    Player_zf = DummyAI(2, "White")

    Player_black = Player(1, "Black")
    Player_white = Player(2, "White")

    # Can choose different modes
    game = Game(Board(15, 15), Player_lv, Player_zf)
    # game = Game(Board(15, 15), Player_zf, Player_lv)
    # game = Game(Board(15, 15), Player_lv, Player_white)
    # game = Game(Board(15, 15), Player_black, Player_lv)
    # game = Game(Board(15, 15), Player_zf, Player_black)
    # game = Game(Board(15, 15), Player_black, Player_zf)

    game.play_one_round()