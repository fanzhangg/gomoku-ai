from unittest import TestCase
from score import ScoreCounter, Chain
from classes import Board


class TestScoreCounter(TestCase):
    def setUp(self):
        self.counter = ScoreCounter(8, 8, 1, 2)

    def test_get_chains_at(self):
        self.fail()

    def test_update_scores(self):
        self.fail()

    def test_is_win(self):
        self.fail()

    def test_get_max_chain_at_step(self):
        counter = ScoreCounter(4, 4, 1, 2)
        board = Board(8, 8)
        board.board = [
            [0, 0, 0, 0],
            [2, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        actual = counter.get_max_chain_at_step(board, (1, 2), (0, 1), 1, 2)
        self.assertEqual(actual.end, {'coord': (1, 0), 'isBlocked': True})
        self.assertEqual(actual.front, {'coord': (1, 4), 'isBlocked': True})
        self.assertIsNone(actual.gap)

        board.board = [
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]
        ]

        actual = counter.get_max_chain_at_step(board, (-1, 4), (1, -1), 1, 2)
        self.assertEqual(actual.end, {'coord': (0, 4), 'isBlocked': True})
        self.assertEqual(actual.front, {'coord': (3, 0), 'isBlocked': False})
        self.assertIsNone(actual.gap)

