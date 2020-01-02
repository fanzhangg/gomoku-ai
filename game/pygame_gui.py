import pygame
from game.board import Board
from player_lv_V2 import PlayerLV2
from os import path

COLOR_BOARD = (255, 180, 0)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

GRID_WIDTH = 45


class GUI:
    def __init__(self):
        self.width = 675
        self.screen = pygame.display.set_mode((self.width + GRID_WIDTH, self.width + GRID_WIDTH))
        pygame.display.set_caption("Gomoku")
        self.screen.fill(COLOR_BOARD)

        self.turn = "black"     # black goes first
        self.cur_player = 2

        self.ai = PlayerLV2(1, "White")

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

