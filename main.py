import pygame
from game.pygame_gui import GUI
from sys import exit

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    game = GUI()
    game.draw_board()

    while True:

        event = pygame.event.poll()

        # Put black key
        if event.type == pygame.MOUSEBUTTONDOWN:
            i, j = pygame.mouse.get_pos()
            if game.turn == "black":
                if 45 <= i <= game.width and 45 <= j <= game.width:
                    i, j = game.get_draw_pos(i, j)
                    game.draw_stone(i, j)

                if game.is_win(2, (i, j)):  # Black wins
                    game.show_win_msg("Black")

        # Put white key
        if event.type == pygame.MOUSEBUTTONUP:
            if game.turn == "white":
                i, j = game.ai_move()
                print(i, j)
                print(f"win: {game.is_win(1, (i, j))}")

                if game.is_win(1, (i, j)):  # White wins
                    game.show_win_msg("White")

        # Close the window
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        pygame.display.update()
