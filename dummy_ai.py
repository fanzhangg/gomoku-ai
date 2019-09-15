from classes import Board


class Chain:
    def __init__(self):
        self.size = 0
        self.front = None
        self.end = None
        self.gap = None
        self.step = None


class DummyAI:
    """
    Strategy: get a pattern such as 2 rows with a 3-stone chains share a same stone
    * 0 0
    * 0 0
    * * *
    - defense
      - 3-stone chain
      - 4-stone chain with one side blocked
      - 2 2-stone chain whose end intersects
        * 0 0
        * 0 0
        0 * *

    - attack
    """
    def __init__(self, id, opponent, stone):
        self.opponent = opponent
        self.id = id
        self.stone = stone
        self.patterns = stone

    def get_available_center_point(self, board: Board):
        x = board.rows // 2
        y = board.cols // 2
        if board.get(x, y) == 0:
            return x, y
        else:
            return x+1, y+1

    def attack(self, board:Board)->tuple:
        pass

    def move(self, board)->tuple:
        defending_point = self.get_defending_point(board, board.last_move)
        if defending_point:
            return defending_point
        else:
            # TODO: implement a defending strategy
            return self.get_empty_point(board)

    def get_empty_point(self, board)->tuple:
        for i in range(board.rows):
            for j in range(board.cols):
                if board.get(i, j) == 0:
                    return i, j

    def get_free_point_around(self, board: Board, x: int, y: int):
        while True:
            if board.get(x, y) == 0:
                return x, y

    def get_defending_point(self, board, coord: tuple)->tuple or None:
        """
        :param board: stone board
        :param coord: the coordinate of the starting point
        :return: the number of the max stones in a chain,
        a tuple of the step such as the chain with the largest stone exists,
        the coord of the gap
        """
        # TODO: handle the case when the stone is on the bound
        steps = [(1, 0), (0, 1), (1, 1), (1, -1)]    # row, col, diagonals
        # Detect four
        for step in steps:
            max_chain = self.get_max_chain_at_step(board, coord, step)
            if max_chain.size == 4:
                if max_chain.gap:   # has a gap
                    return max_chain.gap    # put on the gap
                eyes = self.get_unblocked_eyes(board, max_chain)
                if len(eyes) > 0:   # live/dead four
                    # choose the one relatively close to the center
                    return eyes[0]

        # Detect live three
        for step in steps:
            max_chain = self.get_max_chain_at_step(board, coord, step)
            if max_chain.size == 3:
                if max_chain.gap:   # has a gap
                    return max_chain.gap    # put on the gap
                eyes = self.get_unblocked_eyes(board, max_chain)
                if len(eyes) == 2:  # live three
                    return eyes[0]

        # Detect dead three
        for step in steps:
            max_chain = self.get_max_chain_at_step(board, coord, step)
            if max_chain.size == 3:
                return max_chain.gap
            eyes = self.get_unblocked_eyes(board, max_chain)
            if len(eyes) == 1:
                return eyes[0]

        # Detect two
        for step in steps:
            max_chain = self.get_max_chain_at_step(board, coord, step)
            if max_chain.size == 2:
                return max_chain.gap
            eyes = self.get_unblocked_eyes(board, max_chain)
            if len(eyes) > 0:
                return eyes[0]

        # Detect one
        for step in steps:
            max_chain = self.get_max_chain_at_step(board, coord, step)
            eyes = self.get_unblocked_eyes(board, max_chain)
            if len(eyes) > 0:
                return eyes[0]

        return None

    def get_unblocked_eyes(self, board, chain: Chain)->list:
        """
        :param board:
        :param chain: a chain maximize the number of stones in the direction
        :return: a list of tuples of the unblocked eyes
        """
        # check in front of stone
        eyes = []
        row, col = chain.front
        row, col = row + chain.step[0], col + chain.step[1]
        try:
            if board.get(row, col) == 0:
                eyes.append((row, col))
        except IndexError:
            pass
        row, col = chain.end[0] - chain.step[0], chain.end[1] - chain.step[1]
        try:
            if board.get(row, col) == 0:
                eyes.append((row, col))
        except IndexError:
            pass
        return eyes

    def get_max_chain_at_step(self, board, coord: tuple, step: tuple)->Chain:
        """
        :param board: stone board
        :param coord: the coordinate of the starting point
        :param step: a tuple specifying the incrementation of the coordinate
        :return: the largest number of stones in a chain (allow one gap) in the direction of the step
        A boolean value to indicate whether the chain has a gap such as 11101
        return 0, None if the chain is blocked by the wall or a black stone
        """
        has_gap = False
        gap_coord = None
        total = 0
        chain = Chain()

        def is_gap(x, y, curr_step):
            """
            :param x: row index
            :param y: col index
            :param curr_step: a tuple of current step
            :return: true if the point (x, y) is 0, no gap has been found, the next point has the value of opponent
            """
            try:
                n = board.get(x+curr_step[0], y+curr_step[1])
            except IndexError:
                return False
            return board.get(x, y) == 0 and not has_gap and n == self.opponent

        # Search positive direction
        row, col = coord
        while 1:    # Increment when searching a point with the same opponent
            try:
                if board.get(row, col) == self.opponent:
                    total += 1
                elif is_gap(row, col, step):    # Keep searching if the point is a gap
                    has_gap = True
                    gap_coord = (row, col)
                else:
                    break
            except IndexError:  # The chain is blocked by the wall when the index out of bound
                break
            row += step[0]
            col += step[1]

        chain.front = (row-step[0], col-step[1])

        # Search negative direction
        row, col = coord

        row -= step[0]  # The original point has been counted
        col -= step[1]
        while 1:
            try:
                if board.get(row, col) == self.opponent:
                    total += 1
                elif is_gap(row, col, (-step[0], -step[1])):
                    has_gap = True
                    gap_coord = (row, col)
                else:
                    break
            except IndexError:
                break
            row -= step[0]
            col -= step[1]

        chain.end = (row+step[0], col+step[1])

        chain.size = total
        chain.gap = gap_coord
        chain.step = step

        return chain
