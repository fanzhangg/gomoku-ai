import copy
from classes import Board


class MoveTree:
    def __init__(self, board: list, move: tuple, is_turn: bool) -> None:
        self.board = board
        self.move = move
        self.score = None
        self.is_turn = is_turn
        self.alpha = -1
        self.beta = 100000
        self.parent = None
        self.siblings = []
        self.children = []

    def add_child(self, child) -> None:
        child.parent = self
        child.siblings.extend(self.children)
        self.children.append(child)

    def remove_child(self, child) -> None:
        self.children.remove(child)
        for kid in self.children:
            kid.siblings.remove(child)

    def set_score(self, score: int) -> None:
        self.score = score

    def is_valid(self) -> bool:
        return self.beta > self.alpha

    def has_evaluated(self):
        for child in self.children:
            if child is None:
                return False
        return True

    def set_alphabeta(self) -> None:
        if self.is_turn:
            for child in self.children:
                if child.score is not None and child.score < self.alpha:
                    self.alpha = child.score
            for sibling in self.siblings:
                if sibling.score is not None and sibling.score > self.beta:
                    self.beta = sibling.score
        else:
            for child in self.children:
                if child.score is not None and child.score > self.beta:
                    self.alpha = child.score
            for sibling in self.siblings:
                if sibling.score is not None and sibling.score < self.alpha:
                    self.beta = sibling.score

    def print_tree(self, tree):
        if tree.children == []:
            print(str(tree.move), end = '')
        print(self.move)
        for child in tree.children:
            print(str(child.move), end = ' ')
            self.print_tree(child)
        print('')
        


class PlayerLV:
    def __init__(self, id: int, stone: str) -> None:
        self.id = id
        self.opp = 3 - id
        self.stone = stone
        self.max_steps = 3

    def extend_in_four_directions(self, board: list, move: tuple) -> dict:
        lis = []
        i = move[0]
        j = move[1]

        cur_row = '3'
        idx_row = [(len(board), len(board))]
        for k in range(len(board)):
            cur_row += str(board[i][k])
            idx_row.append((i, k))
        cur_row += '3'
        idx_row.append((len(board), len(board)))
        lis.append((cur_row, idx_row))

        cur_col = '3'
        idx_col = [(len(board), len(board))]
        for k in range(len(board)):
            cur_col += str(board[k][j])
            idx_col.append((k, j))
        cur_col += '3'
        idx_col.append((len(board), len(board)))
        lis.append((cur_col, idx_col))

        cur_backslash = '3'
        idx_backslash = [(len(board), len(board))]
        for k in range(max(-i, -j), min(len(board) - i, len(board) - j)):
            cur_backslash += str(board[i+k][j+k])
            idx_backslash.append((i+k,j+k))
        cur_backslash += '3'
        idx_backslash.append((len(board), len(board)))
        lis.append((cur_backslash, idx_backslash))

        cur_slash = '3'
        idx_slash = [(len(board), len(board))]
        for k in range(max(-i, j - len(board) + 1), min(len(board) - i, j + 1)):
            cur_slash += str(board[i+k][j-k])
            idx_slash.append((i+k,j-k))
        cur_slash += '3'
        idx_slash.append((len(board), len(board)))
        lis.append((cur_slash, idx_slash))

        return lis

    def obligated_move(self, cur_row: str, idx_row: list) -> list:
        ptn_040_opp = '0' + str(self.opp) * 4 + '0'

        ptn_041_opp = '0' + str(self.opp) * 4 + str(self.id)
        ptn_140_opp = str(self.id) + str(self.opp) * 4 + '0'
        ptn_301_opp = str(self.opp) * 3 + '0' + str(self.opp)
        ptn_103_opp = str(self.opp) + '0' + str(self.opp) * 3
        ptn_202_opp = str(self.opp) * 2 + '0' + str(self.opp) * 2
        ptn_40_opp = '3' + str(self.opp) * 4 + '0'
        ptn_04_opp = '0' + str(self.opp) * 4 + '3'

        ptn_030_opp = '0' + str(self.opp) * 3 + '0'
        ptn_02010_opp = '0' + str(self.opp) * 2 + '0' + str(self.opp) + '0'
        ptn_01020_opp = '0' + str(self.opp) + '0' + str(self.opp) * 2 + '0'

        if ptn_040_opp in cur_row:
            return [-5, idx_row[cur_row.index(ptn_040_opp)]
                    # , idx_row[cur_row.index(ptn_040_opp) + 5]
                    ]

        elif ptn_041_opp in cur_row:
            return [-4, idx_row[cur_row.index(ptn_041_opp)]]
        elif ptn_140_opp in cur_row:
            return [-4, idx_row[cur_row.index(ptn_140_opp) + 5]]
        elif ptn_301_opp in cur_row: 
            return [-4, idx_row[cur_row.index(ptn_301_opp) + 3]]
        elif ptn_103_opp in cur_row:
            return [-4, idx_row[cur_row.index(ptn_103_opp) + 1]]
        elif ptn_202_opp in cur_row:
            return [-4, idx_row[cur_row.index(ptn_202_opp) + 2]]
        elif ptn_40_opp in cur_row:
            return [-4, idx_row[cur_row.index(ptn_40_opp) + 5]]
        elif ptn_04_opp in cur_row:
            return [-4, idx_row[cur_row.index(ptn_04_opp)]]
        
        elif ptn_030_opp in cur_row:
            return [-3, idx_row[cur_row.index(ptn_030_opp)], idx_row[cur_row.index(ptn_030_opp) + 4]]
        elif ptn_02010_opp in cur_row:
            return [-3, idx_row[cur_row.index(ptn_02010_opp)], idx_row[cur_row.index(ptn_02010_opp) + 3], idx_row[cur_row.index(ptn_02010_opp) + 5]]
        elif ptn_01020_opp in cur_row:
            return [-3, idx_row[cur_row.index(ptn_01020_opp)], idx_row[cur_row.index(ptn_01020_opp) + 2], idx_row[cur_row.index(ptn_01020_opp) + 5]]

        return [-1]

    def win_move(self, cur_row: str, idx_row: list) -> int:
        ptn_5_id = str(self.id) * 5

        ptn_040_id = '0' + str(self.id) * 4 + '0'
        ptn_303_id= str(self.id) * 3 + '0' + str(self.id) * 3
        ptn_10301_id = str(self.id) + '0' + str(self.id) * 3 + '0' + str(self.id)
        ptn_20202_id = str(self.id) * 2 + '0' + str(self.id) * 2 + '0' + str(self.id) * 2

        ptn_041_id = '0' + str(self.id) * 4 + str(self.opp)
        ptn_140_id = str(self.opp) + str(self.id) * 4 + '0'
        ptn_301_id = str(self.id) * 3 + '0' + str(self.id)
        ptn_103_id = str(self.id) + '0' + str(self.id) * 3
        ptn_202_id = str(self.id) * 2 + '0' + str(self.id) * 2
        ptn_40_id = '3' + str(self.id) * 4 + '0'
        ptn_04_id = '0' + str(self.id) * 4 + '3'

        ptn_030_id = '0' + str(self.id) * 3 + '0'
        ptn_02010_id = '0' + str(self.id) * 2 + '0' + str(self.id) + '0'
        ptn_01020_id = '0' + str(self.id) + '0' + str(self.id) * 2 + '0'

        if ptn_5_id in cur_row:
            return 10

        elif ptn_040_id in cur_row or ptn_303_id in cur_row or ptn_10301_id in cur_row or ptn_20202_id in cur_row:
            return 5

        elif ptn_041_id in cur_row or ptn_140_id in cur_row or ptn_301_id in cur_row or ptn_103_id in cur_row or ptn_202_id in cur_row or ptn_40_id in cur_row or ptn_04_id in cur_row:
            return 4
        
        elif ptn_030_id in cur_row or ptn_02010_id in cur_row or ptn_01020_id in cur_row:
            return 3

        return -1
    
    def get_moves(self, board: list) -> list:
        moves = []
        move_dic = {}

        extended_board = [[0 for i in range(len(board) + 4)] for j in range(len(board) + 4)]
        for a in range(len(board)):
            for b in range(len(board)):
                extended_board[a+2][b+2] = board[a][b]

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    surround_1 = [extended_board[i-1+2][j-1+2], extended_board[i-1+2][j+2], extended_board[i-1+2][j+1+2], 
                                  extended_board[i+2][j-1+2], extended_board[i+2][j+1+2], 
                                  extended_board[i+1+2][j-1+2], extended_board[i+1+2][j+2], extended_board[i+1+2][j+1+2]]
                    surround_2 = [extended_board[i-2+2][j-2+2], extended_board[i-2+2][j+2], extended_board[i-2+2][j+2+2], 
                                  extended_board[i+2][j-2+2], extended_board[i+2][j+2+2], 
                                  extended_board[i+2+2][j-2+2], extended_board[i+2+2][j+2], extended_board[i+2+2][j+2+2]]
                    if any(surround_1) or self.id in surround_2:

                        # print("possible: " + str((i, j)))

                        new_board = copy.deepcopy(board)
                        new_board[i][j] = self.id
                        row_lis = self.extend_in_four_directions(new_board, (i, j))

                        num_fours = 0
                        num_threes = 0
                        for cur_row in row_lis:
                            sign = self.win_move(cur_row[0], cur_row[1])
                            if sign == 4:
                                num_fours += 1
                            elif sign == 3:
                                num_threes += 1
                            elif sign != -1:
                                move_dic[sign] = [(i, j)]
                        
                        if num_fours >= 2:
                            move_dic[8] = [(i, j)]
                        elif num_fours >= 1 and num_threes >= 1:
                            move_dic[7] = [(i, j)]
                        elif num_threes >= 2:
                            if 6 in move_dic:
                                move_dic[6].append((i, j))
                            else:
                                move_dic[6] = [(i, j)]

                        moves.append((i, j))

                    if any(surround_1) or self.opp in surround_2:
                        row_lis_1 = self.extend_in_four_directions(board, (i, j))

                        for cur_row in row_lis_1:
                            sign = self.obligated_move(cur_row[0], cur_row[1])
                            if sign[0] == -3:
                                if -3 in move_dic:
                                    move_dic[-3].extend(sign[1:])
                                else:
                                    move_dic[-3] = sign[1:]
                            elif sign[0] != -1:
                                move_dic[sign[0]] = sign[1:]

                        new_board = copy.deepcopy(board)
                        new_board[i][j] = self.opp
                        row_lis_2 = self.extend_in_four_directions(new_board, (i, j))

                        num_fours = 0
                        num_threes = 0
                        four_moves = []
                        three_moves = []
                        for cur_row in row_lis_2:
                            sign = self.obligated_move(cur_row[0], cur_row[1])
                            if sign[0] == -4:
                                num_fours += 1
                                four_moves.extend(sign[1:])
                            elif sign[0] == -3:
                                num_threes += 1
                                three_moves.extend(sign[1:])

                        if num_fours >= 2:
                            move_dic[-8] = [(i, j)] + four_moves
                        elif num_fours >= 1 and num_threes >= 1:
                            move_dic[-7] = [(i, j)] + four_moves + three_moves
                        elif num_threes >= 2:
                            if -6 in move_dic:
                                move_dic[-6].append((i, j))
                                move_dic[-6].extend(three_moves)
                            else:
                                move_dic[-6] = [(i, j)] + three_moves

        # print("move_dic: " + str(move_dic))

        for n in [10, -5, -4, 5, 8, 7]:
            if n in move_dic:
                return move_dic[n]
        if -3 in move_dic:
            if  4 in move_dic:
                return move_dic[4] + move_dic[-3]
            else:
                return move_dic[-3]
        for n in [6, -8, -7, -6]:
            if n in move_dic:
                return move_dic[n]

        return moves

    def evaluate_score(self, cur_row: str, move_idx: int) -> int:
        ptn_5_id = str(self.id) * 5
        ptn_040_id = '0' + str(self.id) * 4 + '0'
        ptn_303_id= str(self.id) * 3 + '0' + str(self.id) * 3
        ptn_10301_id = str(self.id) + '0' + str(self.id) * 3 + '0' + str(self.id)
        ptn_20202_id = str(self.id) * 2 + '0' + str(self.id) * 2 + '0' + str(self.id) * 2

        ptn_041_id = '0' + str(self.id) * 4 + str(self.opp)
        ptn_140_id = str(self.opp) + str(self.id) * 4 + '0'
        ptn_301_id = str(self.id) * 3 + '0' + str(self.id)
        ptn_103_id = str(self.id) + '0' + str(self.id) * 3
        ptn_202_id = str(self.id) * 2 + '0' + str(self.id) * 2
        ptn_40_id = '3' + str(self.id) * 4 + '0'
        ptn_04_id = '0' + str(self.id) * 4 + '3'

        ptn_030_id = '0' + str(self.id) * 3 + '0'
        ptn_02010_id = '0' + str(self.id) * 2 + '0' + str(self.id) + '0'
        ptn_01020_id = '0' + str(self.id) + '0' + str(self.id) * 2 + '0'

        ptn_021_opp = '0' + str(self.opp) * 2 + str(self.id)
        ptn_120_opp = str(self.id) + str(self.opp) * 2 + '0'

        # ptn_01010_opp, ptn_

        ptn_130_opp = str(self.id) + str(self.opp) * 3 + '0'
        ptn_031_opp = '0' + str(self.opp) * 3 + str(self.id)
        ptn_02110_opp = '0' + str(self.opp) * 2 + str(self.id) + str(self.opp) + '0'
        ptn_01120_opp = '0' + str(self.opp) + str(self.id) + str(self.opp) * 2 + '0'
        ptn_12010_opp = str(self.id) + str(self.opp) * 2 + '0' + str(self.opp) + '0'
        ptn_02011_opp = '0' + str(self.opp) * 2 + '0' + str(self.opp) + str(self.id)
        ptn_01021_opp = '0' + str(self.opp) + '0' + str(self.opp) * 2 + str(self.id)
        ptn_11020_opp = str(self.id) + str(self.opp) + '0' + str(self.opp) * 2 + '0'

        ptn_020_id = '0' + str(self.id) * 2 + '0'

        ptn_130_id = str(self.opp) + str(self.id) * 3 + '0'
        ptn_031_id = '0' + str(self.id) * 3 + str(self.opp)

        ptn_03_id = '0' + str(self.id) * 3 + '3'
        ptn_30_id = '3' + str(self.id) * 3 + '0'
        ptn_0201_id = '0' + str(self.id) * 2 + '0' + str(self.id) + '3'
        ptn_2010_id = '3' + str(self.id) * 2 + '0' + str(self.id) + '0'
        ptn_0102_id = '0' + str(self.id) + '0' + str(self.id) * 2 + '3'
        ptn_1020_id = '3' + str(self.id) + '0' + str(self.id) * 2 + '0'

        ptn_110_opp = str(self.id) + str(self.opp) + '0'
        ptn_011_opp = '0' + str(self.opp) + str(self.id)

        score = 0
        cur_row_7 = cur_row[max(move_idx - 7, 0): min(move_idx + 8, len(cur_row))]
        cur_row_6 = cur_row[max(move_idx - 6, 0): min(move_idx + 7, len(cur_row))]
        cur_row_5 = cur_row[max(move_idx - 5, 0): min(move_idx + 6, len(cur_row))]
        cur_row_4 = cur_row[max(move_idx - 4, 0): min(move_idx + 5, len(cur_row))]
        cur_row_3 = cur_row[max(move_idx - 3, 0): min(move_idx + 4, len(cur_row))]
        cur_row_2 = cur_row[max(move_idx - 2, 0): min(move_idx + 3, len(cur_row))]

        if ptn_5_id in cur_row_4 or ptn_040_id in cur_row_4 or ptn_303_id in cur_row_6 or ptn_10301_id in cur_row_6 or ptn_20202_id in cur_row_7:
            score += 1000

        elif ptn_030_id in cur_row_3:
            score += 8

        elif ptn_041_id in cur_row_4 or ptn_140_id in cur_row_4 or ptn_301_id in cur_row_4 or ptn_103_id in cur_row_4 or ptn_202_id in cur_row_4 or ptn_40_id in cur_row_4 or ptn_04_id in cur_row_4:
            score += 7

        elif ptn_02010_id in cur_row_4 or ptn_01020_id in cur_row_4:
            score += 6
        
        elif ptn_130_opp in cur_row_4 or ptn_031_opp in cur_row_4 or ptn_02110_opp in cur_row_3 or ptn_01120_opp in cur_row_3:
            score += 5
        elif ptn_12010_opp in cur_row_5 or ptn_01021_opp in cur_row_5 or ptn_02011_opp in cur_row_5 or ptn_11020_opp in cur_row_5:
            score += 4

        elif ptn_021_opp in cur_row_3 or ptn_120_opp in cur_row_3:
            score += 3
        elif ptn_020_id in cur_row_2:
            score += 3
        elif ptn_130_id in cur_row_3 or ptn_031_id in cur_row_3:
            score += 2
        elif ptn_03_id in cur_row_3 or ptn_30_id in cur_row_3 or ptn_0201_id in cur_row_3 or ptn_2010_id in cur_row_3 or ptn_0102_id in cur_row_3 or ptn_1020_id in cur_row_3:
            score += 1
        elif ptn_011_opp in cur_row_2 or ptn_110_opp in cur_row_2:
            score += 1

        return score

    def add_next_opp_moves(self, tree, cur_row: str, idx_row: list, board: list, cur_move: tuple, steps: int) -> None:
        ptn_5_id = str(self.id) * 5
        ptn_040_id = '0' + str(self.id) * 4 + '0'
        ptn_303_id= str(self.id) * 3 + '0' + str(self.id) * 3
        ptn_10301_id = str(self.id) + '0' + str(self.id) * 3 + '0' + str(self.id)
        ptn_20202_id = str(self.id) * 2 + '0' + str(self.id) * 2 + '0' + str(self.id) * 2

        ptn_041_id = '0' + str(self.id) * 4 + str(self.opp)
        ptn_140_id = str(self.opp) + str(self.id) * 4 + '0'
        ptn_301_id = str(self.id) * 3 + '0' + str(self.id)
        ptn_103_id = str(self.id) + '0' + str(self.id) * 3
        ptn_202_id = str(self.id) * 2 + '0' + str(self.id) * 2
        ptn_40_id = '3' + str(self.id) * 4 + '0'
        ptn_04_id = '0' + str(self.id) * 4 + '3'

        ptn_030_id = '0' + str(self.id) * 3 + '0'
        ptn_02010_id = '0' + str(self.id) * 2 + '0' + str(self.id) + '0'
        ptn_01020_id = '0' + str(self.id) + '0' + str(self.id) * 2 + '0'

        move_idx = idx_row.index(cur_move)
        cur_row_7 = cur_row[max(move_idx - 7, 0): min(move_idx + 8, len(cur_row))]
        cur_row_6 = cur_row[max(move_idx - 6, 0): min(move_idx + 7, len(cur_row))]
        cur_row_4 = cur_row[max(move_idx - 4, 0): min(move_idx + 5, len(cur_row))]
        cur_row_3 = cur_row[max(move_idx - 3, 0): min(move_idx + 4, len(cur_row))]

        next_moves = []

        if ptn_5_id in cur_row_4 or ptn_040_id in cur_row_4 or ptn_303_id in cur_row_6 or ptn_10301_id in cur_row_6 or ptn_20202_id in cur_row_7:
            return None

        elif ptn_041_id in cur_row_4:
            next_moves.append(idx_row[cur_row.index(ptn_041_id)])
        elif ptn_140_id in cur_row_4:
            next_moves.append(idx_row[cur_row.index(ptn_140_id) + 5])
        elif ptn_301_id in cur_row_4:
            next_moves.append(idx_row[cur_row.index(ptn_301_id) + 3])
        elif ptn_103_id in cur_row_4:
            next_moves.append(idx_row[cur_row.index(ptn_103_id) + 1])
        elif ptn_202_id in cur_row_4:
            next_moves.append(idx_row[cur_row.index(ptn_202_id) + 2])
        elif ptn_40_id in cur_row_4:
            next_moves.append(idx_row[cur_row.index(ptn_40_id) + 5])
        elif ptn_04_id in cur_row_4:
            next_moves.append(idx_row[cur_row.index(ptn_04_id)])

        elif ptn_030_id in cur_row_3:
            left_idx = cur_row.index(ptn_030_id)
            right_idx = left_idx + 4
            next_moves.append(idx_row[left_idx])
            next_moves.append(idx_row[right_idx])
        elif ptn_02010_id in cur_row_4:
            left_idx = cur_row.index(ptn_02010_id)
            middle_idx = left_idx + 3
            right_idx = left_idx + 5
            next_moves.append(idx_row[left_idx])
            next_moves.append(idx_row[middle_idx])
            next_moves.append(idx_row[right_idx])
        elif ptn_01020_id in cur_row_4:
            left_idx = cur_row.index(ptn_01020_id)
            middle_idx = left_idx + 3
            right_idx = left_idx + 5
            next_moves.append(idx_row[left_idx])
            next_moves.append(idx_row[middle_idx])
            next_moves.append(idx_row[right_idx])

        else:
            return None
        
        for next_move in next_moves:
            next_board = copy.deepcopy(board)
            next_board[next_move[0]][next_move[1]] = self.opp
            next_tree = MoveTree(next_board, next_move, False)
            self.add_next_id_moves(next_tree, next_board, steps + 1)
            tree.add_child(next_tree)

    def add_next_id_moves(self, tree, board: list, steps: int) -> None:
        if steps > self.max_steps:
            return None
        moves = self.get_moves(board)

        for move in moves:
            next_board = copy.deepcopy(board)
            next_board[move[0]][move[1]] = self.id
            row_lis = self.extend_in_four_directions(next_board, move)
            next_tree = MoveTree(next_board, move, True)
            for cur_row in row_lis:
                # could be improved by "only one line with three or four"
                self.add_next_opp_moves(next_tree, cur_row[0], cur_row[1], next_board, move, steps)
            tree.add_child(next_tree)

    def calculate_score(self, tree) -> None:
        if tree.children == []:
            row_lis = self.extend_in_four_directions(tree.board, tree.move)
            # print("row_lis: " + str(row_lis))
            score = 0
            for cur_row in row_lis:
                score += self.evaluate_score(cur_row[0], cur_row[1].index(tree.move))
            tree.set_score(score)
            # print("Now: " + str(tree.move) + ", " + str(score))
        
        elif tree.has_evaluated():
            if tree.is_turn:
                tree.score = tree.alpha
            else:
                tree.score = tree.beta

        for child in tree.children:
            tree.set_alphabeta()
            if child.is_valid():
                self.calculate_score(child)
            # else:
            #     tree.remove_child(child)


    def move(self, board: Board) -> tuple:
        moves = self.get_moves(board.board)
        # print("moves: " + str(moves))
        if len(moves) == 1:
            return moves[0]
        elif len(moves) == 0:
            return (7, 7)

        move_tree = MoveTree(board.board, board.last_move, False)
        self.add_next_id_moves(move_tree, board.board, 0)
        self.calculate_score(move_tree)

        # move_tree.print_tree(move_tree)

        max_score = -1
        max_child = None
        for child in move_tree.children:
            # print("Then: " + str(child.move) + ", " + str(child.score))
            if child.score > max_score:
                max_child = child
                max_score = child.score
        
        return max_child.move



