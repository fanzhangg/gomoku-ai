import math
import numpy as np


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

score_dict_human = {
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



def update_in_four_dirs(tree, board, score_board_ai, score_board_human, move):
    """
    Could be improved by selecting one direction from score board of shape (rows, cols, 4).
    """
    i, j = move
    extended_rows = {}
    extended_points = {}
    for dir in range(4):
        extended_rows[dir] = []
        extended_points[dir] = []
    # count_living_fives = 0
    # count_half_fours = 0
    # count_living_threes = 0


    for k in range(len(board)):
        extended_points[ROW].append((i, k))
        extended_rows[ROW].append(board[i][k])

        extended_points[COLUMN].append((k, j))
        extended_rows[COLUMN].append(board[k][j])

    for k in range(max(-i, -j), min(len(board) - i, len(board) - j)):
        extended_points[BACKSLASH].append((i+k, j+k))
        extended_rows[BACKSLASH].append(board[i+k][j+k])

    for k in range(max(-i, j - len(board) + 1), min(len(board) - i, j + 1)):
        extended_points[SLASH].append((i+k, j-k))
        extended_rows[SLASH].append(board[i+k][j-k])

    for dir in range(4):
        row = [2] + extended_rows[dir] + [2]
        points = extended_points[dir]
        for idx in range(len(points)):
            point = points[idx]
            if board[point] != 1:
                chain = get_chain(row, idx, AI)
                if str(AI) * 5 in chain:
                    tree.winner = AI
                    return 
                score_board_ai[point][dir] = score_dict_ai[chain] if chain in score_dict_ai else 0
            if board[point] != 2:
                chain = get_chain(row, idx, HUMAN)
                if str(HUMAN) * 5 in chain:
                    tree.winner = HUMAN
                    return 
                score_board_human[point][dir] = score_dict_human[chain] if chain in score_dict_human else 0

# 从一个点向一个方向扩散(若发现2则停止搜索)，直到 [cur_num=2 or cur_num=0] and [len(str)>=6 or num(2)=2] 为止。
# 每个点的分数 = 以这个点为起点最长chain的分数
# 若发现连续五个1，则直接return 1000000.
def get_chain(row, idx, id):
    row.append(3-id)
    chain = str(row[idx+1])
    count = 1

    for num in row[idx+2:]:
        chain += str(num)
        count += 1
        if num == 3-id or (num == 0 and count >= 6):
            return chain
