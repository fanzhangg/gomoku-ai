from unittest import TestCase
from classes import Board
from dicky_score_counter import ScoreCounter

class TestScoreCounter(TestCase):
    def setUp(self):
        self.sc = ScoreCounter(1, 2)

    def test_get_max_chain_at_step(self):
        self.fail()

    def test_get_unblocked_eyes(self):
        self.fail()

    def test_get_chain_from_start(self):
        board = Board(1, 5)
        board.board = [
            [0, 1, 1, 0, 1]
        ]
        chain = self.sc.get_chain_from_start(board, (0, 2), (0, 1))
        print(chain.list)
