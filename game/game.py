class Game:
    def __init__(self, board: Board, p1: Player, p2: Player):
        self.board = board
        self.p1 = p1
        self.p2 = p2

    """
    Check whether there is an unbreakable chain of 5 stones at coord such as
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

    def is_win(self, id: int, coord: tuple) -> bool:
        #       row      col     diagonal
        steps = [(0, 1), (1, 0), (1, -1), (1, 1)]
        for step in steps:
            if self.is_chain(id, coord, step) == True:
                return True

    def play_one_round(self):
        self.board.print_board()
        while (1):
            for p in (self.p1, self.p2):
                print(f"It is {p.stone}'s turn'" + "\n")
                row, col = p.move(self.board)
                self.board.put(p.id, row, col)
                print(p.stone + " makes " + str((row, col)) + "\n")
                self.board.print_board()
                if self.is_win(p.id, (row, col)) == True:
                    print(f"OMG, {p.stone} wins!\n")
                    return