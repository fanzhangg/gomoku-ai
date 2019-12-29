from classes import Board


class Chain:
    def __init__(self):
        self.size = 0
        self.front_blocked = True
        self.end_blocked = True
        self.has_gap = False
        self.list = []

    def __str__(self):
        return f"front: {self.front_blocked}, end: {self.end_blocked}, gap: {self.has_gap}, list: {self.list}"


class ScoreCounter:
    def __init__(self, me: int, opponent: int):
        self.me = me
        self.opponent = opponent
        self.score_boards = {
            id: Board(15, 15),  # a board to store our scores
            opponent: Board(15, 15)   # opponent scores
        }

    def get_chain_from_start(self, board: Board, start: (int, int), step: (int, int)):
        """
        Get the max length chain from the start on the direction of the step, allow at most 1 gap
        :param board:
        :param start:
        :param step:
        :return:
        """
        x, y = start
        chain = Chain()

        while True:
            try:
                num = board.get(x, y)
                if num == self.me:
                    chain.size += 1
                elif num == 0:
                    chain.list.append(0)

                    if not board.get(x + step[0], y + step[1]) == 0 and not chain.has_gap:    # first single 0, allow to skip
                        chain.has_gap = True
                    elif chain.has_gap:    # second 0
                        chain.end_blocked = False
                    elif board.get(x + step[0], y + step[1]) == 0:  # 2+ 0s
                        chain.end_blocked = False

                elif num == self.me:    # my stone
                    chain.list.append(num)
                elif num == self.opponent:  # opponent stone
                    chain.list.append(num)
                    chain.end_blocked = False
                    return chain

            except IndexError:  # reach the edge
                chain.list.append(self.opponent)
                chain.end_blocked = True
                return Chain


