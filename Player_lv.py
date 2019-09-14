import copy
from classes import Board

class Player_LV:
    def __init__(self, id: int, stone: str) -> None:
        self.id = id
        self.opp = 3 - id
        self.stone = stone

    def extend_in_four_directions(self, board: list, i: int, j: int, num: int) -> dict:
        dic = {}

        cur_row = ''
        idx_row = []
        for k in range(max(j - num, 0), min(j + num + 1, len(board))):
            cur_row += str(board[i][k])
            idx_row.append((i,k))
        dic[cur_row] = idx_row

        cur_col = ''
        idx_col = []
        for k in range(max(j - num, 0), min(j + num + 1, len(board))):
            cur_col += str(board[k][j])
            idx_col.append((k,j))
        dic[cur_col] = idx_col

        cur_backslash = ''
        idx_backslash = []
        for k in range(max(-num, -i, -j), min(num + 1, len(board) - i, len(board) - j)):
            cur_backslash += str(board[i+k][j+k])
            idx_backslash.append((i+k,j+k))
        dic[cur_backslash] = idx_backslash    

        cur_slash = ''
        idx_slash = []
        for k in range(max(-num, -i, j - len(board) + 1), min(num + 1, len(board) - i, j)):
            cur_slash += str(board[i+k][j-k])
            idx_slash.append((i+k,j-k))
        dic[cur_slash] = idx_slash

        return dic

    def obligated_move(self, cur_row: str, idx_row: list) -> list:
        ptn_040_opp = '0' + str(self.opp) * 4 + '0'

        ptn_041_opp = '0' + str(self.opp) * 4 + str(self.id)
        ptn_140_opp = str(self.id) + str(self.opp) * 4 + '0'
        ptn_301_opp = str(self.opp) * 3 + '0' + str(self.opp)
        ptn_103_opp = str(self.opp) + '0' + str(self.opp) * 3
        ptn_202_opp = str(self.opp) * 2 + '0' + str(self.opp) * 2

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

        if ptn_5_id in cur_row:
            return 6

        elif ptn_040_id in cur_row or ptn_303_id in cur_row or ptn_10301_id in cur_row or ptn_20202_id in cur_row:
            return 5

        elif ptn_041_id in cur_row or ptn_140_id in cur_row or ptn_301_id in cur_row or ptn_103_id in cur_row or ptn_202_id in cur_row:
            return 4

        return -1
    
    def get_moves(self, board: list, row: int, col: int) -> list:
        moves = []
        move_dic = {}

        last_dic = self.extend_in_four_directions(board, row, col, len(board))
        for cur_row in last_dic:
            sign = self.obligated_move(cur_row, last_dic[cur_row])
            if sign[0] != -1:
                move_dic[sign[0]] = sign[1:]


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
                        new_board = copy.deepcopy(board)
                        new_board[i][j] = self.id

                        row_dic = self.extend_in_four_directions(new_board, i, j, len(new_board))

                        win_moves = []
                        for cur_row in row_dic:
                            win_moves.append(self.win_move(cur_row, row_dic[cur_row]))

                        for sig in win_moves:
                            if sig != -1:
                                move_dic[sig] = [(i, j)]

                        moves.append((i, j))

        if 6 in move_dic:
            return move_dic[6]
        elif -5 in move_dic:
            return move_dic[-5]
        elif 5 in move_dic:
            return move_dic[5]
        elif -4 in move_dic:
            return move_dic[-4]
        elif -3 in move_dic:
            if 4 in move_dic:
                return move_dic[4] + move_dic[-3]
            else:
                return move_dic[-3]

        return moves

    def evaluate_score(self, cur_row: str) -> int:
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

        ptn_030_id = '0' + str(self.id) * 3 + '0'
        ptn_02010_id = '0' + str(self.id) * 2 + '0' + str(self.id) + '0'
        ptn_01020_id = '0' + str(self.id) + '0' + str(self.id) * 2 + '0'

        if ptn_5_id in cur_row or ptn_040_id in cur_row or ptn_303_id in cur_row or ptn_10301_id in cur_row or ptn_20202_id in cur_row:
            return 1000

        elif ptn_041_id in cur_row or ptn_140_id in cur_row or ptn_301_id in cur_row or ptn_103_id in cur_row or ptn_202_id in cur_row:
            return 50

        elif ptn_030_id in cur_row or ptn_02010_id in cur_row or ptn_01020_id in cur_row:
            return 30

        else:
            score = 0
            cur_row_2 = cur_row[3:-3]
            cur_row_3 = cur_row[2:-2]
            cur_row_4 = cur_row[1:-1]
            if '0' + str(self.id) * 2 + '0' in cur_row_2:
                score += 3
            if str(self.opp) + str(self.id) * 3 + '0' in cur_row_3 or '0' + str(self.id) * 3 + str(self.opp) in cur_row_3:
                score += 2
            if str(self.id) + str(self.opp) * 2 + str(self.id) in cur_row_3:
                score += 3
            if str(self.id) + str(self.opp) * 3 + '0' in cur_row_4 or '0' + str(self.opp) * 3 + str(self.id) in cur_row_4:
                score += 2
            return score

    def get_score(self, cur_row: str, idx_row: list, new_board: list, steps: int) -> int:
        if steps > 0:
            return self.evaluate_score(cur_row) 

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

        ptn_030_id = '0' + str(self.id) * 3 + '0'
        ptn_02010_id = '0' + str(self.id) * 2 + '0' + str(self.id) + '0'
        ptn_01020_id = '0' + str(self.id) + '0' + str(self.id) * 2 + '0'

        next_moves = []

        if ptn_5_id in cur_row or ptn_040_id in cur_row or ptn_303_id in cur_row or ptn_10301_id in cur_row or ptn_20202_id in cur_row:
            return 1000

        elif ptn_041_id in cur_row:
            next_moves.append(idx_row[cur_row.index(ptn_041_id)])
        elif ptn_140_id in cur_row:
            next_moves.append(idx_row[cur_row.index(ptn_140_id) + 5])
        elif ptn_301_id in cur_row:
            next_moves.append(idx_row[cur_row.index(ptn_301_id) + 3])
        elif ptn_103_id in cur_row:
            next_moves.append(idx_row[cur_row.index(ptn_103_id) + 1])
        elif ptn_202_id in cur_row:
            next_moves.append(idx_row[cur_row.index(ptn_202_id) + 2])

        elif ptn_030_id in cur_row:
            left_idx = cur_row.index(ptn_030_id)
            right_idx = left_idx + 4
            next_moves.append(idx_row[left_idx])
            next_moves.append(idx_row[right_idx])
        elif ptn_02010_id in cur_row:
            left_idx = cur_row.index(ptn_02010_id)
            middle_idx = left_idx + 3
            right_idx = left_idx + 5
            next_moves.append(idx_row[left_idx])
            next_moves.append(idx_row[middle_idx])
            next_moves.append(idx_row[right_idx])
        elif ptn_01020_id in cur_row:
            left_idx = cur_row.index(ptn_01020_id)
            middle_idx = left_idx + 3
            right_idx = left_idx + 5
            next_moves.append(idx_row[left_idx])
            next_moves.append(idx_row[middle_idx])
            next_moves.append(idx_row[right_idx])

        else:
            score = 0
            cur_row_2 = cur_row[3:-3]
            cur_row_3 = cur_row[2:-2]
            cur_row_4 = cur_row[1:-1]
            if '0' + str(self.id) * 2 + '0' in cur_row_2:
                score += 3
            if str(self.opp) + str(self.id) * 3 + '0' in cur_row_3 or '0' + str(self.id) * 3 + str(self.opp) in cur_row_3:
                score += 2
            if str(self.id) + str(self.opp) * 2 + str(self.id) in cur_row_3:
                score += 3
            if str(self.id) + str(self.opp) * 3 + '0' in cur_row_4 or '0' + str(self.opp) * 3 + str(self.id) in cur_row_4:
                score += 2
            return score
        
        scores = []
        for next_move in next_moves:
            next_board = copy.deepcopy(new_board)
            next_board[next_move[0]][next_move[1]] = self.opp
            if len(next_moves) == 1:
                scores.append(self.get_result(next_board, next_move, steps)[1])
            else:
                scores.append(self.get_result(next_board, next_move, steps + 1)[1])
        return max(scores)
        # return (4 - len(scores)) * 10

    def get_result(self, board: list, last_move: tuple, steps: int) -> tuple:
        moves = self.get_moves(board, last_move[0], last_move[1])
        if len(moves) == 1:
            return (moves[0], 1000)

        scores = {}
        for (i, j) in moves:
            # i = move[0]
            # j = move[1]

            new_board = copy.deepcopy(board)
            new_board[i][j] = self.id

            row_dic = self.extend_in_four_directions(new_board, i, j, 5)
            scores[(i, j)] = 0
            for cur_row in row_dic:
                scores[(i, j)] += self.get_score(cur_row, row_dic[cur_row], new_board, steps)
            
        best_move = (7, 8)
        best_score = -1000
        for move in scores:
            if scores[move] > best_score:
                best_move = move
                best_score = scores[move]
        
        return (best_move, best_score)

    def move(self, board: Board) -> tuple:
        step = 0
        return self.get_result(board.board, board.last_move, step)[0]