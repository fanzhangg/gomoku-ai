from tkinter import *
from tkinter import messagebox
from game.player import Player
from ai.player_lv_V4 import PlayerLV4
from game.board import Board


class GUI:
    def __init__(self):
        self.win = Tk()
        self.win.title("Gomoku")

        self.buttons = []
        self.turn = "black"
        self.display()

        self.p1 = PlayerLV4(1, "White")
        self.p2 = Player(2, "Black")
        self.board = Board(15, 15)

        self.win.mainloop()

    def display(self):
        f1 = Frame(self.win, padx=10, pady=10)
        f1.grid(row=1, column=1)

        row = []

        for i in range(15):
            for j in range(15):
                button = Button(f1, text="", width=2, heigh=1, command=lambda i=i, j=j: self.click_button(i, j))
                # button.pack()
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)
            row = []

        # for i in range(len(self.buttons)):
        #     for j in range(len(row)):
        #         print(i, j)
        #         button = self.buttons[i][j]
        #         button.bind("<Button>", lambda i=i, j=j: self.click_button(i, j))
        #         button.bind("<ButtonRelease>", self.put_white)

    def click_button(self, x, y):
        print("click button")

        if self.buttons[x][y]["text"] == "":
            if self.turn == "black":
                self.buttons[x][y]["text"] = "⚫"
                self.board.put(2, x, y)
                if self.is_win(2, (x, y)):
                    messagebox.showinfo("Black wins!", "Do you want to play again?")
                else:
                    self.turn = "white"
            self.put_white()

    def put_white(self):
        print("put white")
        print(self.board.board)
        x, y = self.p1.move(self.board)

        print(f"x: {x}, y: {y}")
        self.board.put(1, x, y)
        self.buttons[x][y]["text"] = "⚪️"
        if self.is_win(1, (x, y)):
            messagebox.showinfo("White wins!", "Do you want to play again?")
        else:
            self.turn = "black"

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
