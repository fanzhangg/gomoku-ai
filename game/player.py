from game.board import Board


class Player:
    def __init__(self, id: int, stone: str):
        self.id = id
        self.stone = stone

    def move(self, board: Board):
        """
        Ask for the user's input until a valid one appears, and then update the board
        :param board:
        :return:
        """
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