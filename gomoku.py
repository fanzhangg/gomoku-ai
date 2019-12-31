import copy
from classes import Board
import random
# from score_counter import eval_board
import math
import numpy as np


MAX_STEPS = 2


class MoveTree:
    def __init__(self, move: tuple, is_turn: bool) -> None:
        self.move = move
        self.score = -math.inf if is_turn else math.inf
        self.is_turn = is_turn # whether is AI's turn
        self.alpha = -math.inf
        self.beta = math.inf
        self.parent = None
        self.children = []

    def add_child(self, child) -> None:
        child.parent = self
        self.children.append(child)

        if self.is_turn:
            child.alpha = self.alpha
        else:
            child.beta = self.beta

    def set_score(self, score: int) -> None:
        self.score = score
        if self.parent.is_turn and self.parent.alpha < score:
            self.parent.alpha = score
        elif not self.parent.is_turn and self.parent.beta > score:
            self.parent.beta = score

    def get_num_leafs(self, tree):
        if tree.children == []:
            return 1
        num = 0
        for child in tree.children:
            num += self.get_num_leafs(child)
        return num
        


class PlayerLV:
    def __init__(self, id: int, stone: str) -> None:
        self.id = id
        self.opp = 3 - id
        self.stone = stone

    def update_in_four_dirs(self, board, score_board_ai, score_board_human, move):
        i, j = move
        
        for k in range(len(board)):
            if k != j:
                point = (i, k)
                if board[point] != self.id:
                    score_board_ai[point] = update_score(board, point, 0, self.id)
                if board[point] != self.opp:
                    score_board_human[point] = update_score(board, point, 0, self.opp)

        for k in range(len(board)):
            if k != i:
                point = (k, j)
                if board[point] != self.id:
                    score_board_ai[point] = update_score(board, point, 1, self.id)
                if board[point] != self.opp:
                    score_board_human[point] = update_score(board, point, 1, self.opp)

        for k in range(max(-i, -j), min(len(board) - i, len(board) - j)):
            if k != 0:
                point = (i+k, j+k)
                if board[point] != self.id:
                    score_board_ai[point] = update_score(board, point, 2, self.id)
                if board[point] != self.opp:
                    score_board_human[point] = update_score(board, point, 2, self.opp)

        for k in range(max(-i, j - len(board) + 1), min(len(board) - i, j + 1)):
            if k != 0:
                point = (i+k, j-k)
                if board[point] != self.id:
                    score_board_ai[point] = update_score(board, point, 3, self.id)
                if board[point] != self.opp:
                    score_board_human[point] = update_score(board, point, 3, self.opp)

        score_board_ai[move] = 0
        score_board_human[move] = 0
        if board[move] != self.id:
            for dir in range(4):
                score_board_ai[move] += update_score(board, move, dir, self.id)
        if board[move] != self.opp:
            for dir in range(4):
                score_board_human[move] += update_score(board, move, dir, self.opp)

    
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


    def build_tree(self, tree, board, score_board_ai, score_board_human, steps: int) -> None:

        # if (len(moves) > 3 and steps <= 0) or len(moves) == 0:
        if steps == MAX_STEPS:
            # score = eval_board(board, self.id, self.opp) - eval_board(board, self.opp, self.id)
            # print(score_board_human)
            score = np.sum(score_board_ai - score_board_human)
            tree.set_score(score)
            # if score < -5000:
            #     print("Leaf score: " + str(steps) + " -- " + str(tree.move) + " -- " + str(score))
            # print("Leaf score: " + str(steps) + " -- " + str(tree.move) + " -- " + str(score))
            return None

        # Current id is 1 when steps is even.
        cur_id = 1 if tree.is_turn else 2

        for move in self.get_moves(board, cur_id):
            next_board = copy.deepcopy(board)
            next_board[move] = cur_id
            next_tree = MoveTree(move, not tree.is_turn)

            # if tree.alpha < tree.beta: # If the next tree is valid, add child. Else skip.
            if 1:
                tree.add_child(next_tree)
                # next_tree.parent = tree
                # tree.children.append(next_tree)

                # if tree.is_turn:
                #     next_tree.alpha = tree.alpha
                # else:
                #     next_tree.beta = tree.beta

                next_score_board_ai = copy.deepcopy(score_board_ai)
                next_score_board_human = copy.deepcopy(score_board_human)
                self.update_in_four_dirs(next_board, next_score_board_ai, next_score_board_human, move)

                self.build_tree(next_tree, next_board, next_score_board_ai, next_score_board_human, steps + 1)
            # else:
            #     print("haha")

        # print(tree.is_turn)
        if tree.parent:
            if tree.is_turn: # If the next turn is AI, choose the move with max score.
                tree.set_score(max(child.score for child in tree.children))
            else:
                tree.set_score(min(child.score for child in tree.children))

        # final_score = tree.score
        # for child in tree.children:
        #     if child.score == final_score:
        #         print("steps, cur_move, next_move, score: " + str(steps) + " -- " + str(tree.move) + " -- " + str(child.move) + " -- " + str(final_score))


    def move(self, board: Board) -> tuple:
        moves = self.get_moves(board.board, self.id)
        # print(moves)
        if len(moves) == 0:
            return (board.rows//2, board.rows//2)

        move_tree = MoveTree(board.last_move, True)
        score_board_ai = np.zeros((board.rows, board.rows))
        score_board_human = np.zeros((board.rows, board.rows))
        for i in range(board.rows):
            for j in range(board.rows):
                for dir in range(4):
                    score_board_ai[i][j] += update_score(board.board, (i,j), dir, self.id)
                    score_board_human[i][j] += update_score(board.board, (i,j), dir, self.opp)

        self.build_tree(move_tree, board.board, score_board_ai, score_board_human, 0)

        # print("num_of_leafs: " + str(move_tree.get_num_leafs(move_tree)))

        max_score = move_tree.children[0].score
        max_children = [move_tree.children[0]]
        for child in move_tree.children[1:]:

            # print("Then: " + str(child.move) + ", " + str(child.score))

            if child.score is not None:
                if child.score > max_score:
                    max_children = [child]
                    max_score = child.score
                elif child.score == max_score:
                    max_children.append(child)
        
        # Should be stochastic
        return random.choice(max_children).move


# 从一个点向一个方向扩散(若发现2则停止搜索)，直到 [cur_num=2 or cur_num=0] and [len(str)>=6 or num(2)=2] 为止。
# 每个点的分数 = 以这个点为起点最长chain的分数
# 若发现连续五个1，则直接return 100000.
score_dict = {
        # half one
        "000012": 1, "210000": 1, 

        # living one
        "010000": 10, "001000": 10, "000100": 10, "000010": 10, 

        # half two
        "0100010": 10, # "0010010" and "0001010" are repeated with living two
        "000112": 10, "001012": 10, "010012": 10, 
        "211000": 10, "210100": 10, "210010": 10, "2100010": 10, 
        "2100012": 10, 
        
        # living two
        "011000": 100, "010100": 100, "010010": 100, "001100": 100, "001010": 100, "000110": 100, 

        # half three
        "0100110": 100, "0101010": 100, "0110010": 100, 
        "001112": 100, "010112": 100, "011012": 100, "0100112": 100, # "011102" and "201110" are already considered by "2011102"
        "211100": 100, "211010": 100, "210110": 100, "2110010": 100, "2101010": 100, "2100110": 100, 
        "2110012": 100, "2101012": 100, "2100112": 100, 

        # living three
        "011100": 1000, "001110": 1000, "010110": 1000, "011010": 1000, 

        # half four
        "0101110": 1000, "0110110": 1000, "0111010": 1000, 
        "011112": 1000, "0101112": 1000, "0110112": 1000, "0111012": 1000, 
        "211110": 1000, "2101110": 1000, "2110110": 1000, "2111010": 1000, 
        "2101112": 1000, "2110112": 1000, "2111012": 1000, 
        
        # living four
        "011110": 10000
        }

def update_score(board, pivot, dir, id):
    i,j = pivot
    row = []

    if dir == 0: # row
        row = board[i, j:]
    elif dir == 1: # col
        row = board[i:, j]
    elif dir == 2: # backslash
        row = board.diagonal(i - j)[min(i,j):]
    elif dir == 3: # slash
        row = np.fliplr(board).diagonal(j - i)[min(i,j):]

    # print(row)

    return get_one_dir_score(row, id)


def get_one_dir_score(row, id):
    opp = 3-id
    row = np.append(row, [opp])
    chain = str(row[0])
    count = 1

    # len(chain) <= 6
    # while row[count] == id or count < 6:
    #     chain += str(row[count])
    #     if row[count] == opp:
    #         break
    #     count += 1

    for num in row[1:]:
        chain += str(num)
        count += 1
        if num == opp:
            break
        if num == 0 and count >= 6:
            break

    # print(chain)

    # if len(chain) == 6:
    #     print(chain)

    new_chain = ""
    if id == 2:
        for i in range(len(chain)):
            if chain[i] != "0":
                new_chain += str(3 - int(chain[i]))
            else:
                new_chain += chain[i]
    else:
        new_chain = chain

    # print(new_chain)

    # if new_chain[0] == "1":
    # if new_chain[-1] == "1":
        # print(new_chain)

    if "11111" in new_chain:
        # print(new_chain)
        return 1000000

    if new_chain in score_dict:
        # print(new_chain)
        return score_dict[new_chain]
    else:
        return 0

a = [2,1,1,1,1,1,0,0,0]
b = [[0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,1,0,0,0,0,0,0],
     [0,0,0,0,1,2,2,0,0,0],
     [0,0,0,0,0,1,0,0,0,0],
     [0,0,0,0,0,0,1,0,0,0],
     [0,0,0,0,0,0,0,1,0,0],
     [0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0]]
b = np.array(b)
# print(get_one_dir_score(a, 1))
r = update_score(b, (2,2), 2, 1)
print(r)




