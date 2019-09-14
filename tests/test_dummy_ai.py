from dummy_ai import DummyAI, Chain
from go import Board, Player
import unittest


class TestGetMaxChainAtStep(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI(1, "Black")

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

    def test_get_unblocked_eyes(self):
        board = Board(1, 5)
        board.board = [[2, 1, 1, 1, 0]]

        chain = self.ai.get_max_chain_at_step(board, (0, 1), (0, 1))
        eyes = self.ai.get_unblocked_eyes(board, chain)
        self.assertEqual([(0, 4)], eyes)

        board = Board(1, 5)
        board.board = [[0, 1, 1, 1, 0]]

        chain = self.ai.get_max_chain_at_step(board, (0, 1), (0, 1))
        eyes = self.ai.get_unblocked_eyes(board, chain)
        self.assertEqual([(0, 4), (0, 0)], eyes)


# class TestDummyAi(unittest.TestCase):
#     def test_get_max_chain_stones(self):
#         # test blocked cases
#         # - block by the wall
#         board = Board(4, 4)
#         board.board = [
#             [1, 0, 0, 0],
#             [0, 1, 0, 0],
#             [0, 0, 1, 0],
#             [0, 0, 0, 0]]
#         ai = DummyAI(1, "white")
#         actual, coord = ai.get_max_chain_at_step(board, (1, 1), (1, 1))
#         self.assertEqual(0, actual)
#
#         actual, coord = ai.get_max_chain_at_step(board, (0, 0), (1, 1))
#         self.assertEqual(0, actual)
#
#         actual, coord = ai.get_max_chain_at_step(board, (2, 2), (1, 1))
#         self.assertEqual(0, actual)
#
#         board = Board(4, 4)
#         board.board = [
#             [0, 0, 0, 0],
#             [0, 1, 0, 0],
#             [0, 0, 1, 0],
#             [0, 0, 0, 1]]
#         ai = DummyAI(1, "white")
#         actual, coord = ai.get_max_chain_at_step(board, (1, 1), (1, 1))
#         self.assertEqual(0, actual)
#
#         actual, coord = ai.get_max_chain_at_step(board, (0, 0), (1, 1))
#         self.assertEqual(0, actual)
#
#         actual, coord = ai.get_max_chain_at_step(board, (2, 2), (1, 1))
#         self.assertEqual(0, actual)
#
#         # - block by another stone
#         board = Board(4, 4)
#         board.board = [
#             [2, 0, 0, 0],
#             [0, 1, 0, 0],
#             [0, 0, 1, 0],
#             [0, 0, 0, 0]]
#         ai = DummyAI(1, "white")
#         actual, coord = ai.get_max_chain_at_step(board, (1, 1), (1, 1))
#         self.assertEqual(0, actual)
#
#         actual, coord = ai.get_max_chain_at_step(board, (0, 0), (1, 1))
#         self.assertEqual(0, actual)
#
#         actual, coord = ai.get_max_chain_at_step(board, (2, 2), (1, 1))
#         self.assertEqual(0, actual)
#
#         board = Board(4, 4)
#         board.board = [
#             [0, 0, 0, 0],
#             [0, 1, 0, 0],
#             [0, 0, 1, 0],
#             [0, 0, 0, 2]]
#         ai = DummyAI(1, "white")
#         actual, coord = ai.get_max_chain_at_step(board, (1, 1), (1, 1))
#         self.assertEqual(0, actual)
#
#         actual, coord = ai.get_max_chain_at_step(board, (0, 0), (1, 1))
#         self.assertEqual(0, actual)
#
#         actual, coord = ai.get_max_chain_at_step(board, (2, 2), (1, 1))
#         self.assertEqual(0, actual)
#
#         # - test block and with a gap
#         board2 = Board(6, 6)
#         board2.board = [
#             [0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0],
#             [0, 0, 0, 0, 1, 0],
#             [0, 0, 0, 0, 0, 2]
#         ]
#         actual, coord = ai.get_max_chain_at_step(board2, (1, 1), (1, 1))
#         self.assertEqual(0, actual)
#         self.assertEqual(None, coord)
#
#         actual, coord = ai.get_max_chain_at_step(board2, (4, 4), (1, 1))
#         self.assertEqual(0, actual)
#         self.assertEqual(None, coord)
#
#         # test continuous chain
#         board2.board  = [
#             [0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0],
#             [0, 0, 1, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0],
#             [0, 0, 0, 0, 1, 0],
#             [0, 0, 0, 0, 0, 0]
#         ]
#
#         actual, coord = ai.get_max_chain_at_step(board2, (2, 2), (1, 1))
#         self.assertEqual(4, actual)
#         self.assertEqual(None, coord)
#
#         actual, coord = ai.get_max_chain_at_step(board2, (1, 1), (1, 1))
#         self.assertEqual(4, actual)
#         self.assertEqual(None, coord)
#
#         actual, coord = ai.get_max_chain_at_step(board2, (4, 4), (1, 1))
#         self.assertEqual(4, actual)
#         self.assertEqual(None, coord)
#
#         # test chain with a gap
#         board2.board = [
#             [0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0],
#             [0, 0, 0, 0, 1, 0],
#             [0, 0, 0, 0, 0, 0]
#         ]
#         actual, coord = ai.get_max_chain_at_step(board2, (1, 1), (1, 1))
#         self.assertEqual(3, actual)
#         self.assertEqual((2, 2), coord)
#
#         actual, coord = ai.get_max_chain_at_step(board2, (4, 4), (1, 1))
#         self.assertEqual(3, actual)
#         self.assertEqual((2, 2), coord)
#
#         # test chain with 2 gaps
#         board3 = Board(7, 7)
#         board3.board = [
#             [0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 1, 0],
#             [0, 0, 0, 0, 0, 0, 0]
#         ]
#         actual, coord = ai.get_max_chain_at_step(board3, (1, 1), (1, 1))
#         self.assertEqual(2, actual)
#         self.assertEqual((2, 2), coord)
#
#         actual, coord = ai.get_max_chain_at_step(board3, (5, 5), (1, 1))
#         self.assertEqual(2, actual)
#         self.assertEqual((4, 4), coord)


# class TestMaxChainAtPoint(unittest.TestCase):
#     def setUp(self):
#         self.ai = DummyAI(1, "Black")
#         self.board = Board(10, 10)
#
#     def test_single_chain(self):
#         self.board.board = [
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         ]
#         point_max, step, gap = self.ai.get_max_chain_at_point(self.board, (1, 1))
#         self.assertEqual(4, point_max)
#         self.assertEqual((1, 1), step)
#         self.assertEqual(None, gap)
#
#     def test_multiple_chain(self):
#         self.board.board = [
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#             [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#             [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         ]
#         point_max, step, gap = self.ai.get_max_chain_at_point(self.board, (2, 2))
#         self.assertEqual(4, point_max)
#         self.assertEqual((1, 1), step)
#         self.assertEqual(None, gap)
#
#     def test_blocked_chain(self):
#         self.board.board = [
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         ]
#         point_max, step, gap = self.ai.get_max_chain_at_point(self.board, (2, 2))
#         self.assertEqual(2, point_max)
#         self.assertEqual((0, 1), step)
#         self.assertEqual(None, gap)
#
#     def test_gap_chain(self):
#         self.board.board = [
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#         ]
#         point_max, step, gap = self.ai.get_max_chain_at_point(self.board, (2, 2))
#         self.assertEqual(3, point_max)
#         self.assertEqual((1, 1), step)
#         self.assertEqual((3, 3), gap)


class TestGetDefendingPoint(unittest.TestCase):
    def setUp(self):
        self.ai = DummyAI(1, "Black")

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
        board.board = [[0, 1, 1, 1, 0]]
        point = self.ai.get_defending_point(board, (0, 1))
        self.assertEqual((0, 4), point)

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
