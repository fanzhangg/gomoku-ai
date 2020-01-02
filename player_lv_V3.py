import copy
from game.board import Board
import random
# from score_counter import eval_board
import math
import numpy as np


MAX_STEPS = 2
AI = 1
HUMAN = 2
ROW = 0
COLUMN = 1
BACKSLASH = 2
SLASH = 3


score_dict_ai = {
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
        "0101110": 10000, "0110110": 10000, "0111010": 10000, 
        "011112": 10000, "0101112": 10000, "0110112": 10000, "0111012": 10000, 
        "211110": 10000, "2101110": 10000, "2110110": 10000, "2111010": 10000, 
        "2101112": 10000, "2110112": 10000, "2111012": 10000, 

        # living four
        "011110": 100000
        
        # # half four
        # "0101110": 1000, "0110110": 1000, "0111010": 1000, 
        # "011112": 1000, "0101112": 1000, "0110112": 1000, "0111012": 1000, 
        # "211110": 1000, "2101110": 1000, "2110110": 1000, "2111010": 1000, 
        # "2101112": 1000, "2110112": 1000, "2111012": 1000, 

        # # living four
        # "011110": 10000
        }

score_dict_huamn = {
        # half one
        "000021": 1, "120000": 1, 

        # living one
        "020000": 10, "002000": 10, "000200": 10, "000020": 10, 

        # half two
        "0200020": 10, 
        "000221": 10, "002021": 10, "020021": 10, 
        "122000": 10, "120200": 10, "120020": 10, "1200020": 10, 
        "1200021": 10, 
        
        # living two
        "022000": 100, "020200": 100, "020020": 100, "002200": 100, "002020": 100, "000220": 100, 

        # half three
        "0200220": 100, "0202020": 100, "0220020": 100, 
        "002221": 100, "020221": 100, "022021": 100, "0200221": 100, 
        "122200": 100, "122020": 100, "120220": 100, "1220010": 100, "1202020": 100, "1200220": 100, 
        "1220021": 100, "1202021": 100, "1200221": 100, 

        # living three
        "022200": 1000, "002220": 1000, "020220": 1000, "022020": 1000, 

        # half four
        "0202220": 1000, "0220220": 1000, "0222020": 1000, 
        "022221": 1000, "0202221": 1000, "0220221": 1000, "0222021": 1000, 
        "122220": 1000, "1202220": 1000, "1220220": 1000, "1222020": 1000, 
        "1202221": 1000, "1220221": 1000, "1222021": 1000, 

        # living four
        "022220": 10000
        }


class MoveTree:
    def __init__(self, move: tuple, is_turn: bool) -> None:
        self.move = move
        self.score = -math.inf if is_turn else math.inf
        self.is_turn = is_turn # whether is AI's turn
        self.alpha = -math.inf
        self.beta = math.inf
        self.parent = None
        self.children = []
        self.winner = 0

    def add_child(self, child) -> None:
        child.parent = self
        self.children.append(child)

        if self.is_turn:
            child.alpha = self.alpha
        else:
            child.beta = self.beta

    def set_score(self, score: int) -> None:
        self.score = score

        if self.parent:
            if not self.is_turn and self.parent.alpha < score:
                self.parent.alpha = score
            elif self.is_turn and self.parent.beta > score:
                self.parent.beta = score
            
    def get_num_leafs(self, tree):
        if tree.children == []:
            return 1
        num = 0
        for child in tree.children:
            num += self.get_num_leafs(child)
        return num
        

class PlayerLV3:
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


    def build_tree(self, tree, board, score_board_ai, score_board_human, steps: int) -> None:

        if steps == MAX_STEPS:
            score = np.sum(score_board_ai - score_board_human)
            tree.set_score(score)

            # print("Leaf score: " + str(steps) + " -- " + str(tree.move) + " -- " + str(score))

            return None

        if tree.winner:
            tree.set_score(math.inf) if tree.winner == 1 else tree.set_score(-math.inf)

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
        score_board_ai = np.zeros((board.rows, board.rows, 4))
        score_board_human = np.zeros((board.rows, board.rows, 4))
        for i in range(board.rows):
            for j in range(board.rows):
                for dir in range(4):
                    score_board_ai[i][j][dir] += update_score(move_tree, board.board, (i,j), AI, dir)
                    score_board_human[i][j][dir] += update_score(move_tree, board.board, (i,j), HUMAN, dir)

        self.build_tree(move_tree, board.board, score_board_ai, score_board_human, 0)

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
        
        # for child in max_children:
        #     print(child.move)
        # Should be stochastic
        return random.choice(max_children).move
        


def update_in_four_dirs(tree, board, score_board_ai, score_board_human, move):
    """
    Could be improved by selecting one direction from score board of shape (rows, cols, 4).
    """
    i, j = move

    for k in range(len(board)):
        point = (i, k)
        if board[point] != 1:
            score_board_ai[point][ROW] = update_score(tree, board, point, AI, ROW)
            # print(score_board_ai[point])
        if board[point] != 2:
            score_board_human[point][ROW] = update_score(tree, board, point, HUMAN, ROW)
            # print(score_board_human[point])

        point = (k, j)
        if board[point] != 1:
            score_board_ai[point][COLUMN] = update_score(tree, board, point, AI, COLUMN)
        if board[point] != 2:
            score_board_human[point][COLUMN] = update_score(tree, board, point, HUMAN, COLUMN)

    for k in range(max(-i, -j), min(len(board) - i, len(board) - j)):
        point = (i+k, j+k)
        if board[point] != 1:
            score_board_ai[point][BACKSLASH] = update_score(tree, board, point, AI, BACKSLASH)
        if board[point] != 2:
            score_board_human[point][BACKSLASH] = update_score(tree, board, point, HUMAN, BACKSLASH)

    for k in range(max(-i, j - len(board) + 1), min(len(board) - i, j + 1)):
        point = (i+k, j-k)
        if board[point] != 1:
            score_board_ai[point][SLASH] = update_score(tree, board, point, AI, SLASH)
        if board[point] != 2:
            score_board_human[point][SLASH] = update_score(tree, board, point, HUMAN, SLASH)

def update_score(tree, board, pivot, id, dir):
    i,j = pivot
    row = []
    dir_score= 0

    if dir == ROW:
        row = board[i, j:]
    
    elif dir == COLUMN:
        row = board[i:, j]

    elif dir == BACKSLASH:
        for k in range(min(len(board) - i, len(board) - j)):
            point = (i+k, j+k)
            row.append(board[point])

    elif dir == SLASH:
        for k in range(min(len(board) - i, j + 1)):
            point = (i+k, j-k)
            row.append(board[point])

    dir_score = get_one_dir_score(row, id)

    if dir_score >= 1000000:
        tree.winner = id
    return dir_score

# 从一个点向一个方向扩散(若发现2则停止搜索)，直到 [cur_num=2 or cur_num=0] and [len(str)>=6 or num(2)=2] 为止。
# 每个点的分数 = 以这个点为起点最长chain的分数
# 若发现连续五个1，则直接return 1000000.
def get_one_dir_score(row, id):
    opp = 3-id
    row = np.append(row, [opp])
    chain = str(row[0])
    count = 1

    for num in row[1:]:
        chain += str(num)
        count += 1
        if num == opp:
            break
        if num == 0 and count >= 6:
            break
    
    # print(chain)

    if str(id) * 5 in chain:
        # tree.winner = id
        return 1000000

    if id == 1 and chain in score_dict_ai:
            return score_dict_ai[chain]
    elif id == 2 and chain in score_dict_huamn:
            return score_dict_huamn[chain]

    return 0

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



