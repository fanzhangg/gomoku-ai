import pygame
from game.board import Board
from player_lv_V3 import PlayerLV3
from os import path

COLOR_BOARD = (255, 180, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

GRID_WIDTH = 45


class GUI:
    def __init__(self):
        self.width = 675
        self.height = 700
        self.screen = pygame.display.set_mode((self.width + GRID_WIDTH, self.height + GRID_WIDTH))
        pygame.display.set_caption("Gomoku")
        self.screen.fill(COLOR_BOARD)

        self.turn = "black"     # black goes first
        self.cur_player = 2

        self.ai = PlayerLV3(1, "White")

        self.steps = {  # keep track of the steps of each stone
            "white": [],
            "black": []
        }

        self.board = Board(15, 15)

    def draw_board(self):
        for i in range(1, 16):
            pygame.draw.line(self.screen, COLOR_BLACK,
                             [GRID_WIDTH * i, GRID_WIDTH], [GRID_WIDTH * i, self.width], 2)
            pygame.draw.line(self.screen, COLOR_BLACK,
                             [GRID_WIDTH, GRID_WIDTH * i], [self.width, GRID_WIDTH * i], 2)

        pygame.draw.circle(self.screen, COLOR_BLACK, [GRID_WIDTH * 8, GRID_WIDTH * 8], 8)

    @staticmethod
    def get_draw_pos(x, y):
        draw_x, draw_y = x - x % GRID_WIDTH, y - y % GRID_WIDTH
        if x % GRID_WIDTH > GRID_WIDTH / 2:     # close to the right point
            draw_x += GRID_WIDTH

        if y % GRID_WIDTH > GRID_WIDTH / 2: # close to the bottom point
            draw_y += GRID_WIDTH
        return draw_x, draw_y

    def draw_stone(self, x: int, y: int):
        # Do not put stone in occupied position
        if (x, y) in self.steps["white"]:
            return
        if (x, y) in self.steps["black"]:
            return

        if self.turn == "white":
            color = COLOR_WHITE
            img_path = path.abspath("imgs/white.png")
            img = pygame.image.load(img_path)
        else:
            color = COLOR_BLACK
            img_path = path.abspath("imgs/black.png")
            img = pygame.image.load(img_path)

        scaled_img = pygame.transform.smoothscale(img, (GRID_WIDTH // 3 * 2, GRID_WIDTH // 3 * 2))

        self.screen.blit(scaled_img, (x - GRID_WIDTH // 3, y - GRID_WIDTH // 3))

        self.steps[self.turn].append((x, y))

        i, j = x // GRID_WIDTH - 1, y // GRID_WIDTH - 1   # index of the stone in the board
        self.board.put(self.cur_player, i, j)

        # Switch the turn
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

        # Switch the current player
        if self.cur_player == 1:
            self.cur_player = 2
        elif self.cur_player == 2:
            self.cur_player = 1

    def ai_move(self):
        # Assume ai is 1 by default
        if self.cur_player == 1:
            i, j = self.ai.move(self.board)
            x, y = (i + 1) * GRID_WIDTH, (j + 1) * GRID_WIDTH
            self.draw_stone(x, y)
            return i, j

    def is_win(self, stone_num: int, coord: tuple) -> bool:
        """
        check whether the player wins the game when put a stone at the coord
        me: 1 for black stone, 2 for white stone
        coord: (row, col)
        return: true if wins, else false
        """

        def is_chain(stone_num: int, coord: tuple, step: tuple):
            """
            Check whether there is an unbreakable chain of 5 stones at coord such as
            the coordinates of the adjacent stone is the coordinate of the stone +/- step
            :return: true if there is a chain of 5 stones, else false
            """
            total = 0
            row, col = coord

            for i in range(5):
                if total >= 5:
                    return True
                try:
                    if self.board.get(row, col) == stone_num:
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
                    if self.board.get(row, col) == stone_num:
                        total += 1
                    else:
                        break
                except IndexError:
                    break
                row -= step[0]
                col -= step[1]

            return False

        #       row      col     diagonal
        steps = [(0, 1), (1, 0), (1, -1), (1, 1)]
        for step in steps:
            if is_chain(stone_num, coord, step):
                return True

    def show_win_msg(self, win_stone: str):
        pygame.font.init()
        my_font = pygame.font.SysFont("Arial", 30)
        text_surface = my_font.render(f"{win_stone} Wins!", True, COLOR_BLACK)
        text_rect = text_surface.get_rect(center=(self.width/2, self.height))
        self.screen.blit(text_surface, text_rect)
