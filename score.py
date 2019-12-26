from classes import Board


class Chain:
    def __init__(self, size=0, front={"coord": (-1, -1), "isBlocked": False},
                 end={"coord": (-1, -1), "isBlocked": False}, gap=None, step=None):
        self.size = 0
        self.front = {"coord": (-1, -1), "isBlocked": False}
        self.end = {"coord": (-1, -1), "isBlocked": False}
        self.gap = None
        self.step = None


class Patterns:
    def __init__(self):
        self.one = set()
        self.two = set()
        self.three = set()
        self.four = set()
        self.five = set()


class Scores:
    def __init__(self):
        self.one = 10
        self.two = 100
        self.three = 1000
        self.four = 10000
        self.five = 100000
        self.blocked_one = 1
        self.blocked_two = 10
        self.blocked_three = 100
        self.blocked_four = 1000


class ScoreBoard:
    """
    A matrix to keep track of the score of each grid
    """
    def __init__(self, rows: int, cols: int):
        # TODO: implement the matrix as a dictionary to optimize the efficiency
        self.board = [[0 for _ in range(rows)] for _ in range(cols)]
        self.rows = rows
        self.cols = cols
        self.total_score = 0

    def print_board(self) -> None:
        pass

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

    def put(self, score: int, row: int, col: int):
        if row < 0 or row >= self.rows:
            raise IndexError("row out of bound")
        if col < 0 or col >= self.cols:
            raise IndexError("col out of bound")
        self.board[row][col] = score


class ScoreCounter:
    def __init__(self, rows: int, cols: int, me: int, opponent: int):
        self.scores = ScoreBoard(rows, cols)
        self.id = me
        self.opponent = opponent

    def get_chains_at(self, board: Board, coord: tuple)->[Chain]:
        pass

    def update_scores(self, chains: [Chain]):
        pass

    def is_win(self, board: Board, coord: tuple)->bool:
        pass

    def get_max_chain_at_step(self, board, coord: tuple, step: tuple, target: int, opponent: int)->Chain:
        """
        :param board: stone board
        :param coord: the coordinate of the starting point
        :param step: a tuple specifying the incrementation of the coordinate
        :return: the largest number of stones in a chain (allow one gap) in the direction of the step
        A boolean value to indicate whether the chain has a gap such as 11101
        return 0, None if the chain is blocked by the wall or a black stone
        """

        total = 0
        chain = Chain()

        def is_gap(x, y):
            try:
                n = board.get(x + step[0], y + step[1])   # Get next stone
            except IndexError:
                return False
            return board.get(x, y) == 0 and not chain.gap and n == self.opponent

        # Search positive direction
        row, col = coord
        while True:    # Increment when searching a point with the same opponent
            try:
                cur_value = board.get(row, col)
                if cur_value == target:
                    total += 1
                elif is_gap(row, col):    # Keep searching if the point is a gap
                    chain.gap = (row, col)
                elif cur_value == opponent:     # The front is blocked by the opponent
                    chain.front["isBlocked"] = True
                    break
                else:
                    break
            except IndexError:  # The chain is blocked by the wall when the index out of bound
                chain.front["isBlocked"] = True    # The front is blocked
                break
            row += step[0]  # Go to next point
            col += step[1]

        chain.front["coord"] = (row, col)   # Get the position of the point in front of the chain

        # Search negative direction
        row, col = coord

        row -= step[0]  # The original point has been counted, avoid counting it again
        col -= step[1]
        while True:
            try:
                cur_value = board.get(row, col)
                if cur_value == target:     # Has a target stone
                    total += 1
                elif is_gap(row, col):  # Is a gap
                    chain.gap = (row, col)
                elif cur_value == opponent:     # Blocked by the opponent
                    chain.end["isBlocked"] = True
                    break
                else:
                    break
            except IndexError:  # Blocked by the wall
                chain.end["isBlocked"] = True
                break
            row -= step[0]
            col -= step[1]

        chain.end["coord"] = (row, col)

        chain.size = total
        chain.step = step

        return chain

    # def eval_scores(patterns: Patterns):
    #     score = Scores()
    #     return score.one * len(patterns.one) + score.two * len(patterns.two)
    #
    #
    # def eval_total_scores(my: Patterns, opp: Patterns):
    #     return eval_scores(my) + eval_scores(opp)



