import numpy as np

def split_row_by_oppo(row: list, id: int, oppo: int):
    """
    Split row by oppo or 00+
    :param row:
    :param id:
    :param oppo:
    :return:
    """
    frags = []
    frag = []
    for i in range(len(row)):
        num = row[i]
        if num == oppo:  # encounter a oppo stone
            if not frag == [] and 0 in frag:  # the chain has a gap, so it is alive
                frags.append(frag)
                frag = []
        else:   # is 0 or self id
            frag.append(num)

        if i == len(row) - 1:  # reach the end of the row
            if not frag == [] and 0 in frag:
                frags.append(frag)
    return frags
    # frags = []
    # frag = [oppo]
    # for i in range(len(row)):
    #     num = row[i]
    #     if num == id:
    #         frag.append(num)
    #     elif num == 0 and i+1 < len(row) and not row[i+1] == 0:
    #         frag.append(0)
    #     elif num == 2:
    #         frag.append(2)
    #         frags.append(frag)
    #         frag = []
    #     else:
    #         frags.append(frag)
    #         frag = []
    # return frags


def split_row_by_multi_0(frags):
    """
    Split the row by 00+
    :param frags: a list of fragment in the row, each fragment is a list of number representing the stone in the grid
    :return:
    """
    chains = []
    for row in frags:
        sub_chains = []
        li = []
        is_chain = False

        if not row[0] == 0:
            li = [2]

        for i in range(len(row)):
            num = row[i]

            if not is_chain and num == 0:
                continue
            elif not is_chain and not num == 0:
                is_chain = True

            if num == 0 and i < len(row) - 1 and row[i+1] == 0:
                sub_chains.append(li)
                li = []
                is_chain = False
            elif i == len(row) - 1:
                if not num == 0:
                    li.append(num)
                    li.append(2)
                sub_chains.append(li)
            else:
                li.append(num)
        chains.extend(sub_chains)
    return chains


def split_by_single_0(chain, id: int, oppo: int):
    chains = []
    new_chain = Chain(True, 0, [])
    for i in range(len(chain)):
        num = chain[i]
        if num == oppo:
            new_chain.is_alive = False

        if num == id:
            new_chain.li.append(num)

        if (num == 0 or i == len(chain) - 1) and not new_chain.li == []:
            new_chain.length = len(new_chain.li)
            chains.append(new_chain)
            new_chain = Chain(True, 0, [])
    return chains


def combine_tokens(chains):
    re_chains = []
    for i in range(len(chains) - 1):
        chain1 = chains[i]
        chain2 = chains[i+1]
        is_alive = chain1.is_alive and chain2.is_alive
        length = len(chain1.li) + len(chain2.li)
        chain = Chain(is_alive, length, [])
        re_chains.append(chain)
    return re_chains


class Chain:
    def __init__(self, is_alive: bool, len: int, li: list):
        self.is_alive = is_alive
        self.length = len
        self.li = li

    def __str__(self):
        return f"is_alive: {self.is_alive}, length: {self.length}, li: {self.li}"


def parse_frag(frag: list, id: int):
    tokens = []

    chain = Chain(True, 0)
    start_int = 0
    while True:
        if not frag[start_int] == 0:
            chain.is_alive = False
        for i in range(start_int, len(frag)):
            num = frag[i]
            if num == id:
                chain.length += 1
            elif num == 0 and frag[i+1] == 0:   # multi-0s
                pass


def eval_solid_chain(chain: [int], id: int, oppo: int)->int:
    is_alive = True
    length = 0

    for x in chain:
        if x == oppo:
            is_alive = False
        elif x == id:
            length += 1

    return get_score(length, is_alive)


def eval_row(row: [int], id: int, oppo: int)->int:
    """
    Parse a list of stones on a row to a list of chain on the row
    :param row: a list of stones on a row
    :return: a list of chain on the row, each chain is a Chain object, storing its length and if it is blocked
    """
    frags = split_row_by_oppo(row, id, oppo)
    new_rows = split_row_by_multi_0(frags)

    total_score = 0

    for row in new_rows:
        if 0 not in row:    # The frag does not have 0 gap
            chain_score = eval_solid_chain(row, id, oppo)
            total_score += chain_score
            continue

        chains_by_single_0 = split_by_single_0(row, id, oppo)

        chains_in_frag = combine_tokens(chains_by_single_0)
        for chain in chains_in_frag:    # The frag has 0 gaps
            chain_score = get_score(chain.length, chain.is_alive)
            total_score += chain_score / 10     # regress to a previous case
        # chains.extend(chains_in_frag)
    return total_score


def get_score(length: int, is_alive: bool)->int:
    if length > 5:
        return 100000
    if length < 1:
        return 0
    return scores_dict[length][is_alive]


scores_dict = {
    1: {False: 0, True: 10},
    2: {False: 10, True: 100},
    3: {False: 100, True: 1000},
    4: {False: 1000, True: 10000},
    5: {False: 100000, True: 100000}
}


# def eval_row(row: [int], id: int, oppo: int):
#     total_score = 0
#     chains = parse_row(row, id, oppo)
#     for chain in chains:
#         chain_score = scores_dict[chain.length][chain.is_alive]
#         total_score += chain_score
#     return total_score


def eval_board(board, id: int, oppo: int):
    """
    :param board: an numpy 2d-array
    :param id:
    :param oppo:
    :return: The total score of the board
    """
    total_score = 0
    num_rows = len(board)

    for row in board:
        row_score = eval_row(row, id, oppo)
        oppo_row_score = eval_row(row, oppo, id)
        print(f"oppo row score: {oppo_row_score}")
        total_score = total_score + row_score - oppo_row_score

    for j in range(num_rows):
        col = board[:, j]

        col_score = eval_row(col, id, oppo)
        oppo_col_score = eval_row(col, oppo, id)
        total_score = total_score + col_score - oppo_col_score

        print(f"oppo col score: {oppo_col_score}")

    diags = [board[::-1,:].diagonal(i) for i in range(-num_rows+1, num_rows)]
    diags.extend(board.diagonal(i) for i in range(num_rows-1, -num_rows, -1))
    for diag in diags:
        diag_score = eval_row(diag, id, oppo)
        oppo_diag_score = eval_row(diag, oppo, id)
        total_score = total_score + diag_score - oppo_diag_score

        print(f"oppo diag score: {oppo_diag_score}")

    return total_score


# test_row = [1, 0, 1, 0, 1, 1, 0, 1, 2, 2, 1, 0, 1, 1, 0, 0, 1, 2]
test_board = np.array([
    [1, 1, 1, 1, 0],
    [0, 2, 2, 2, 0],
    [0, 0, 2, 0, 0],
    [0, 2, 0, 1, 0],
    [0, 0, 0, 0, 1]
])
test_row = [0, 1, 1, 1, 2, 1, 0]
score = eval_board(test_board, 1, 2)
# score = eval_row(test_row, 1, 2)
print(score)
