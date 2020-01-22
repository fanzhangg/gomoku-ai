import copy
from game.board import Board
from ai.lv_helpers import *
import random
# from score_counter import eval_board
import math
import numpy as np


MAX_STEPS = 2
        

class PlayerLV4:
    def __init__(self, id: int, stone: str) -> None:
        self.id = 1
        self.opp = 2
        self.stone = stone

    
    def get_moves(self, board, id: int) -> list:
        moves = []
        num_rows = len(board)

        twos = np.full((2,num_rows), 0, dtype=int)
        twos_plus = np.full((num_rows+2,2), 0, dtype=int)
        extended_board = np.concatenate((board, twos), axis=0)
        extended_board = np.concatenate((extended_board, twos_plus), axis=1)

        for i in range(num_rows):
            for j in range(num_rows):
                if board[i][j] == 0:
                    surround_1 = [extended_board[i-1][j-1], extended_board[i-1][j], extended_board[i-1][j+1], 
                                  extended_board[i][j-1], extended_board[i][j+1], 
                                  extended_board[i+1][j-1], extended_board[i+1][j], extended_board[i+1][j+1]]
                    surround_2 = [extended_board[i-2][j-2], extended_board[i-2][j], extended_board[i-2][j+2], 
                                  extended_board[i][j-2], extended_board[i][j+2], 
                                  extended_board[i+2][j-2], extended_board[i+2][j], extended_board[i+2][j+2]]

                    if any(surround_1) or id in surround_2:
                        moves.append((i, j))

        return moves

    
    # def update_possible_moves(self, moves, id)


    def build_tree(self, tree, board, score_board_ai, score_board_human, steps: int) -> None:

        if steps == MAX_STEPS:
            score = np.sum(score_board_ai - score_board_human)
            tree.set_score(score)

            # print("Leaf score: " + str(steps) + " -- " + str(tree.move) + " -- " + str(score))

            return None

        if tree.winner:
            tree.set_score(math.inf) if tree.winner == 1 else tree.set_score(-math.inf)
            return None

        # Current id is 1 when steps is even.
        cur_id = 1 if tree.is_turn else 2

        for move in self.get_moves(board, cur_id):

            if tree.alpha < tree.beta: # If the next tree is valid, add child. Else skip.
            # if 1:
                next_tree = MoveTree(move, not tree.is_turn)
                tree.add_child(next_tree)

                next_board = copy.deepcopy(board)
                next_board[move] = cur_id

                next_score_board_ai = copy.deepcopy(score_board_ai)
                next_score_board_human = copy.deepcopy(score_board_human)
                update_in_four_dirs(next_tree, next_board, next_score_board_ai, next_score_board_human, move)

                self.build_tree(next_tree, next_board, next_score_board_ai, next_score_board_human, steps + 1)
            # else:
            #     print("haha")

        if tree.is_turn: # If the next turn is AI, choose the move with max score.
            tree.set_score(max([child.score for child in tree.children]))
        else:
            tree.set_score(min([child.score for child in tree.children]))

        final_score = tree.score
        for child in tree.children:
            if child.score == final_score:
                print("steps, cur_move, next_move, score: " + str(steps) + " -- " + str(tree.move) + " -- " + str(child.move) + " -- " + str(final_score))


    def move(self, board: Board) -> tuple:

        moves = self.get_moves(board.board, self.id)
        # board.print_board()
        # print(moves)
        if len(moves) == 0:
            return (board.rows//2, board.rows//2)

        move_tree = MoveTree(board.last_move, True)

        self.build_tree(move_tree, board.board, board.score_board_ai, board.score_board_human, 0)

        # print("num_of_leafs: " + str(move_tree.get_num_leafs(move_tree)))

        max_score = move_tree.children[0].score
        max_children = [move_tree.children[0]]
        for child in move_tree.children[1:]:
            if child.score is not None:
                if child.score > max_score:
                    max_children = [child]
                    max_score = child.score
                elif child.score == max_score:
                    max_children.append(child)
        
        # Should be stochastic
        return random.choice(max_children).move
        
    
    # print(chain)

    # if dir_score >= 1000000:
    #     tree.winner = id


# b = [[0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,1,0,0,1,0,0,0],
#      [0,0,0,0,1,2,2,0,0,0],
#      [0,0,0,0,1,1,1,0,0,0],
#      [0,0,0,1,0,0,1,0,0,0],
#      [0,0,0,0,0,0,0,1,0,0],
#      [0,0,0,0,0,0,0,0,0,0],
#      [0,0,0,0,0,0,0,0,0,0]]
# b = np.array(b)
# r = update_score(None, b, (4,5), 3, 1)
# print(r)

board = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,2,2,2,0,0,0,0,0,0],
         [0,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

board = np.array(board)

# print(board)

# rows = len(board)
# move_tree = MoveTree((-1,-1), True)
# score_board_ai = np.zeros((rows, rows), dtype=int)
# score_board_human = np.zeros((rows, rows), dtype=int)
# for i in range(rows):
#     for j in range(rows):
#         score_board_ai[i][j] += update_score(move_tree, board, (i,j), 1)
#         score_board_human[i][j] += update_score(move_tree, board, (i,j), 2)

# print(score_board_ai)
# print()
# print(score_board_human)
# print()

# board[(4,3)] = 1
# update_in_four_dirs(move_tree, board, score_board_ai, score_board_human, (4,3))

# print(score_board_ai)
# print()
# print(score_board_human)
# print()

# board[(7,5)] = 2
# update_in_four_dirs(move_tree, board, score_board_ai, score_board_human, (7,5))

# print(score_board_ai)
# print()
# print(score_board_human)



