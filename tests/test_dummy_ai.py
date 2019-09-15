from dummy_ai import DummyAI
from go import Board
import unittest


class TestGetMaxChainAtStep(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI(2, 1, "Black")

    def test_continuous_chain(self):
        board = Board(4, 4)
        board.board = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0]]
        chain = self.ai.get_max_chain_at_step(board, (1, 1), (1, 1))
        self.assertEqual((0, 0), chain.end)
        self.assertEqual((2, 2), chain.front)
        self.assertEqual(3, chain.size)
        self.assertEqual(None, chain.gap)

    def test_gap_chain(self):
        board = Board(1, 10)
        board.board = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1]]
        chain = self.ai.get_max_chain_at_step(board, (0, 1), (0, 1))
        self.assertEqual((0, 3), chain.front)
        self.assertEqual((0, 1), chain.end)
        self.assertEqual(2, chain.size)
        self.assertEqual((0, 2), chain.gap)


class TestGetDefendingPoint(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI(2, 1, "Black")

    def test_get_1_unblocked_eyes(self):
        board = Board(1, 5)
        board.board = [[2, 1, 1, 1, 0]]

        chain = self.ai.get_max_chain_at_step(board, (0, 1), (0, 1))
        eyes = self.ai.get_unblocked_eyes(board, chain)
        self.assertEqual([(0, 4)], eyes)

        board = Board(4, 4)
        board.board = [
            [0, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        chain = self.ai.get_max_chain_at_step(board, (1, 1), (0, 1))
        eyes = self.ai.get_unblocked_eyes(board, chain)
        self.assertEqual([(1, 3)], eyes)

    def test_get_2_unblocked_eyes(self):
        board = Board(4, 4)
        board.board = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
        chain = self.ai.get_max_chain_at_step(board, (1, 1), (0, 1))
        eyes = self.ai.get_unblocked_eyes(board, chain)
        self.assertEqual([(1, 3), (1, 0)], eyes)

        board = Board(1, 5)
        board.board = [[0, 1, 1, 1, 0]]

        chain = self.ai.get_max_chain_at_step(board, (0, 1), (0, 1))
        eyes = self.ai.get_unblocked_eyes(board, chain)
        self.assertEqual([(0, 4), (0, 0)], eyes)

    def test_live_four(self):
        board = Board(1, 6)
        board.board = [
            [0, 1, 1, 1, 1, 0]
        ]
        point = self.ai.get_defending_point(board, (0, 1))
        self.assertEqual((0, 5), point)

    def test_dead_four(self):
        board = Board(1, 6)
        board.board = [[0, 1, 1, 1, 1, 2]]
        point = self.ai.get_defending_point(board, (0, 1))
        self.assertEqual((0, 0), point)

    def test_gap_four(self):
        board = Board(1, 6)
        board.board = [[0, 1, 0, 1, 1, 1]]
        point = self.ai.get_defending_point(board, (0, 1))
        self.assertEqual((0, 2), point)

    def test_live_three(self):
        board = Board(1, 5)
        board.board = [[0, 1, 1, 1, 0, 0, 0, 0]]
        point = self.ai.get_defending_point(board, (0, 1))
        self.assertEqual((0, 4), point)

        board2 = Board(5, 5)
        board2.board = [
            [0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        point = self.ai.get_defending_point(board2, (1, 1))
        self.assertEqual((4, 4), point)

    def test_dead_three(self):
        board = Board(1, 5)
        board.board = [[0, 1, 1, 1, 2]]
        point = self.ai.get_defending_point(board, (0, 1))
        self.assertEqual(None, point)

    def test_gap_three(self):
        board = Board(1, 5)
        board.board = [[0, 1, 0, 1, 1]]
        point = self.ai.get_defending_point(board, (0, 1))
        self.assertEqual((0, 2), point)

    def test_two(self):
        board = Board(1, 5)
        board.board = [[0, 1, 1, 0, 0]]
        point = self.ai.get_defending_point(board, (0, 1))
        self.assertEqual(None, point)


class TestIsDoubleIntersection(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI(2, 1, "Black")

    def test_double_two(self):
        board = Board(5, 7)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        actual = self.ai.is_double_intersection(board, 1, 3)
        self.assertTrue(actual)

    def test_double_two_with_gap(self):
        board = Board(6, 9)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        actual = self.ai.is_double_intersection(board, 1, 4)
        self.assertTrue(actual)

    def test_double_dead_three(self):
        board = Board(6, 9)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2]
        ]
        actual = self.ai.is_double_intersection(board, 1, 4)
        self.assertTrue(actual)

    def test_failed_case(self):
        board = Board(6, 9)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1]
        ]
        actual = self.ai.is_double_intersection(board, 1, 4)
        self.assertFalse(actual)


class TestHasDoubleIntersection(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI(2, 1, "Black")

    def test_double_two(self):
        board = Board(5, 7)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        actual = self.ai.get_double_intersection(board)
        self.assertEqual((1, 3), actual)

    def test_double_two_with_gap(self):
        board = Board(6, 9)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        actual = self.ai.get_double_intersection(board)
        self.assertEqual((1, 4), actual)

    def test_double_dead_three(self):
        board = Board(6, 9)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 2]
        ]
        actual = self.ai.get_double_intersection(board)
        self.assertEqual((1, 4), actual)

    def test(self):
        board = Board(9, 9)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def test_failed_case(self):
        board = Board(6, 9)
        board.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1]
        ]
        actual = self.ai.get_double_intersection(board)
        self.assertEqual(None, actual)
