class Board:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.last_move = (7, 7)
        self.board = [[0 for i in range(cols)] for j in range(rows)]    # row major board
        self.sign_dic = {0: "_", 1: "1", 2: "2"}
    
    def print_board(self) -> None:
        print("  ", end = "")
        for k in range(self.rows):
            if 0 <= k and k < 10:
                print(str(k), end = " ")
            else:
                print(str(k), end = "")
        print("")
        for i in range(self.rows):
            if 0 <= i and i < 10:
                print(str(i), end = " ")
            else:
                print(str(i), end = "")
            for j in range(self.cols):
                print(self.sign_dic[self.board[i][j]], end = " ")
            print("")
        print("")

    def clear(self) -> None:
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = 0

    def get(self, row: int, col: int):
        if row < 0 or row >= self.rows:
            raise IndexError("row out of bound")
        if col < 0 or col >= self.cols:
            raise IndexError("col out of bound")
        return self.board[row][col]

    def put(self, id: int, row: int, col: int):
        if row < 0 and row >= self.rows:
            raise IndexError("row out of bound")
        if col < 0 and col >= self.cols:
            raise IndexError("col out of bound")
        self.board[row][col] = id
        self.last_move = (row, col)

class Player:
    def __init__(self, id: int, stone: str):
        self.id = id
        self.stone = stone

    def move(self, board: Board):
        while 1:
            coord = input(">")
            coord = coord.split(" ")
            row = coord[0]
            try:
                col = coord[1]
            except IndexError:
                print("col is invalid")
                continue
            try:
                row = int(row)
            except ValueError:
                print("row is not an int")
                continue
            try:
                col = int(col)
            except ValueError:
                print("col is not an int")
                continue
            if row < 0 or row >= board.rows:
                print("row out of bound")
                continue
            if col < 0 or col >= board.cols:
                print("col out of bound")
                continue
            
            if board.get(row, col) != 0:
                print(f"({row}, {col}) has been occupied")
                continue
            return row, col


class Game:
    def __init__(self, board: Board, p1: Player, p2: Player):
        self.board = board
        self.p1 = p1
        self.p2 = p2

    """
    Check wether there is an unbreakable chain of 5 stones at coord such as
    the coordinates of the adjacent stone is the coordinate of the stone +/- step
    :return: true if there is a chain of 5 stones, else false
    """
    def is_chain(self, id: int, coord: tuple, step: tuple):
        total = 0
        row, col = coord

        for i in range(5):
            if total >= 5:
                return True
            try:
                if self.board.get(row, col) == id:
                    total += 1
                else:
                    break
            except IndexError:
                break
            row += step[0]
            col += step[1]

        row, col = coord
        row -= step[0]
        col -= step[1]

        for i in range(5):
            if total >= 5:
                return True
            try:
                if self.board.get(row, col) == id:
                    total += 1
                else:
                    break
            except IndexError:
                break
            row -= step[0]
            col -= step[1]
        
        return False

    """
    check whether the player wins the game when put a stone at the coord
    id: 1 for black stone, 2 for white stone
    coord: (row, col)
    return: true if wins, else false
    """
    def is_win(self, id: int, coord: tuple)->bool:
        #       row      col     diagonal
        steps = [(0, 1), (1, 0), (1, -1), (1, 1)]
        for step in steps:
            if self.is_chain(id, coord, step) == True:
                return True

    def play_one_round(self):
        print(" * * * * * * Gomoku Game Start * * * * * * \n")
        self.board.print_board()
        while (1):
            for p in (self.p1, self.p2):
                print(f"It is {p.stone}'s turn'" + "\n")
                row, col = p.move(self.board)

                if not isinstance(row, int) or not isinstance(col, int) or row < 0 or col < 0 or row > self.board.rows - 1 or col > self.board.cols - 1:
                    print( p.stone + " gave an invalid move!")
                    return

                self.board.put(p.id, row, col)
                print("Player " + p.stone + " makes " + str((row, col)) + "\n")
                self.board.print_board()
                if self.is_win(p.id, (row, col)) == True:
                    print(f" * * * * * * Player '{p.stone}' Wins! * * * * * * \n")
                    print("Wanna start a new game? ('y' to restart)")
                    if_new = input(">")
                    if if_new == 'y' or if_new == 'Y':
                        self.board.clear()
                        break
                    else:
                        return 
