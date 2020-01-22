import numpy as np
from ai.lv_helpers import MoveTree, update_in_four_dirs


class Board:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.last_move = (-1, -1)
        self.board = np.zeros((rows, cols), dtype=int)  # row major board
        self.score_board_ai = np.zeros((rows, rows, 4), dtype=int)
        self.score_board_human = np.zeros((rows, rows, 4), dtype=int)
        self.sign_dic = {0: "_", 1: "1", 2: "2"}

    def print_board(self) -> None:
        print("  ", end="")
        for k in range(self.rows):
            if 0 <= k < 10:
                print(str(k), end=" ")
            else:
                print(str(k), end="")
        print("")
        for i in range(self.rows):
            if 0 <= i < 10:
                print(str(i), end=" ")
            else:
                print(str(i), end="")
            for j in range(self.cols):
                print(self.sign_dic[self.board[i][j]], end=" ")
            print("")
        print("")

    def clear(self) -> None:
        self.board.fill(0)

    def get(self, row: int, col: int):
        if row < 0 or row >= self.rows:
            raise IndexError("row out of bound")
        if col < 0 or col >= self.cols:
            raise IndexError("col out of bound")
        return self.board[row][col]

    def put(self, stone_num: int, row: int, col: int):
        if row < 0 or row >= self.rows:
            raise IndexError("row out of bound")
        if col < 0 or col >= self.cols:
            raise IndexError("col out of bound")
        self.board[row][col] = stone_num
        self.last_move = (row, col)
        update_in_four_dirs(MoveTree(self.last_move, stone_num == 1), self.board, self.score_board_ai, self.score_board_human, self.last_move)

