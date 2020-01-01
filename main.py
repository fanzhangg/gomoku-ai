import pygame
from game.pygame_gui import GUI
import time

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()



    game = GUI()

    game.draw_board()

    while True:
        event = pygame.event.poll()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if game.turn == "black":
                if 45 <= x <= game.width and 45 <= y <= game.width:
                    x, y = game.get_draw_pos(x, y)
                    game.draw_stone(x, y)

        if game.turn == "white":
            game.ai_move()

        pygame.display.update()
