import unittest
from go import Board, Game, Player

class TestBoard(unittest.TestCase):
    def test_print(self):
        board = Board(15, 15)
        print(board)
        board.print_board()

class TestGame(unittest.TestCase):
    def test_is_chain(self):
        board = Board(1, 5)
        p1 = Player(1, "Black")
        p2 = Player(2, "White")
        game = Game(board, p1, p2)
        self.assertTrue(game.is_chain(0, (0, 2), (0, 1)))
        self.assertFalse(game.is_chain(0, (0, 3), (1, 0)))
        self.assertFalse(game.is_chain(1, (0, 2), (0, 1)))
     
    def test_is_win(self):
        coords = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

        
if __name__ == '__main__':
    unittest.main()