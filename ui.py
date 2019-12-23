#Frank Zhang
#COMP 123 Lian Duan
# This is a cute Gomoku cheese game that you can play with your friends!


# ------------------ import statements -------------#
from tkinter import *
from PIL import ImageTk, Image
import os

# ----------------- global variables --------------#


def createboard():
    boardrow=[]
    board=[]
    for x in range(15):
        for y in range(15):
            boardrow.append("O")
        board.append(boardrow)
        boardrow=[]
    return board


board = createboard()
friend_win = None
button = None
listButtons = []
times = 0
win = ""


# ------------------ function definitions ---------- #

# main GUI
def friendGUI():
    '''Take no input, the main function
    This function creates a Tkinter window,
    including a board with 15*15 buttons, two lables indicating the turn and the winner, a undo button and a new button.'''


    global friend_win
    global button
    global listButtons
    global x
    global y
    global button_new
    global button_undo
    global l_turn
    global l_pic
    global times

    #create the window
    friend_win = Tk()
    friend_win.title("Octocorn Gokuma")

    #create the frame 1 with buttons for the board
    f1 = Frame(friend_win, padx=10, pady=10)
    f1.grid(row=1,column=1)

    #create the board with 15*15 buttons
    listButtons = []
    listrow = []


    for x in range(15):
        for y in range(15):

            button = Button(f1,text="",width=2,height=1,command=lambda x=x, y=y: click_button(x,y))
            button.grid(row=x, column=y)
            listrow.append(button)

    #put buttons to the list listButtons
        listButtons.append(listrow)
        listrow = []

    #create frame 2 with the image and text labels and the new and undo buttons
    f2 = Frame(friend_win,padx=10, pady=10)
    f2.grid(row=1,column=2)

    #create the image label
    img = ImageTk.PhotoImage(Image.open("Octocorn_Black.png"))
    l_pic = Label(f2, image=img)
    l_pic.grid(row=1, column=1)

    #create the text label
    l_turn = Label(f2,text="Black, your turn!",width=20)
    l_turn.grid(row=2, column=1,pady=10)

    #create the undo button
    button_undo = Button(f2,text="Undo",width=4,command=button_undo)
    button_undo.grid(row=3, column=1,pady=10)


    #create the new button
    button_new = Button(f2,text="New",width=4,command=button_new)
    button_new.grid(row=4, column=1,pady=10)


    friend_win.mainloop()


#create the function for checking who wins the game

def check_win(aboard):
    """check if there are 5 identical letter in a row, column or diagonal in the board and indicate who wins the game"""
    global win
    global board
    global button_signal
    global l_turn
    global l_pic
    global f2
    global button
    global listButtons

    #check five indentical letters in a row
    for row in range(15):
        for col in range(11):
            if board[row][col]==board[row][col+1]==board[row][col+2]==board[row][col+3]==board[row][col+4]=="B":


                win="black"

                #Change the text of label
                l_turn["text"] = "And the winner is ... BLACK!"
                #change the color of text of the buttons
                listButtons[row][col]["fg"]="red"
                listButtons[row][col+1]["fg"] = "red"
                listButtons[row][col+2]["fg"] = "red"
                listButtons[row][col+3]["fg"] = "red"
                listButtons[row][col+4]["fg"] = "red"


            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] == board[row][col + 4] == "W":
                win="white"

                l_turn["text"] = "And the winner is ... WHITE!"

                listButtons[row][col]["fg"] = "red"
                listButtons[row][col + 1]["fg"] = "red"
                listButtons[row][col + 2]["fg"] = "red"
                listButtons[row][col + 3]["fg"] = "red"
                listButtons[row][col + 4]["fg"] = "red"

    # check five indentical letters in a column
    for row in range(11):
        for col in range(15):
            if board[row][col]==board[row+1][col]==board[row+2][col]==board[row+3][col]==board[row+4][col]=="B":
                win="black"

                l_turn["text"]="And the winner is ... BLACK!"

                listButtons[row][col]["fg"] = "red"
                listButtons[row+1][col]["fg"] = "red"
                listButtons[row+2][col]["fg"] = "red"
                listButtons[row+3][col]["fg"] = "red"
                listButtons[row+4][col]["fg"] = "red"

            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == board[row+4][col] == "W":
                win="white"

                l_turn["text"]="And the winner is ... WHITE!"

                listButtons[row][col]["fg"] = "red"
                listButtons[row + 1][col]["fg"] = "red"
                listButtons[row + 2][col]["fg"] = "red"
                listButtons[row + 3][col]["fg"] = "red"
                listButtons[row + 4][col]["fg"] = "red"

    #check five indentical letters in a upward diagonal
    for row in range(11):
        for col in range(11):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == board[row+4][col+4] == "B":
                win = "black"

                l_turn["text"] = "And the winner is ... BLACK!"

                listButtons[row][col]["fg"] = "red"
                listButtons[row+1][col+1]["fg"] = "red"
                listButtons[row+2][col+2]["fg"] = "red"
                listButtons[row + 3][col + 3]["fg"] = "red"
                listButtons[row + 4][col + 4]["fg"] = "red"

            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == board[row+4][col+4] == "W":
                win = "white"

                l_turn["text"] = "And the winner is ... WHITE!"

                listButtons[row][col]["fg"] = "red"
                listButtons[row + 1][col + 1]["fg"] = "red"
                listButtons[row + 2][col + 2]["fg"] = "red"
                listButtons[row + 3][col + 3]["fg"] = "red"
                listButtons[row + 4][col + 4]["fg"] = "red"

    # check five indentical letters in a downward diagonal
    for row in range(4,15):
        for col in range(11):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == board[row-4][col+4] == "B":
                win = "black"

                l_turn["text"] = "And the winner is ... BLACK!"

                listButtons[row][col]["fg"] = "red"
                listButtons[row-1][col+1]["fg"] = "red"
                listButtons[row - 2][col + 2]["fg"] = "red"
                listButtons[row - 3][col + 3]["fg"] = "red"
                listButtons[row - 4][col + 4]["fg"] = "red"

            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == board[row-4][col+4] == "W":
                win = "white"

                l_turn["text"] = "And the winner is ... WHITE!"

                listButtons[row][col]["fg"] = "red"
                listButtons[row - 1][col + 1]["fg"] = "red"
                listButtons[row - 2][col + 2]["fg"] = "red"
                listButtons[row - 3][col + 3]["fg"] = "red"
                listButtons[row - 4][col + 4]["fg"] = "red"

# click_button function
def click_button(x,y):
    '''When clicking a button, change the text of the button, the text and image labels, the letter in the board'''
    global listButtons
    global times
    global board
    global row
    global col
    global l_pic
    global f2
    global img
    global win
    global button_undo

    row = x
    col = y


    if listButtons[x][y]["text"]=="" and win == "":

        #check if it is white or black turn
        if times%2 == 0:

            #change the text of the button
            listButtons[x][y]["text"]="⬤"
            #change the text in the board
            board[x][y] = "B"
            #change the text of the label
            l_turn["text"]="White, your turn!"
            #change the image
            img2 = ImageTk.PhotoImage(Image.open("Octocorn_White.png"))
            l_pic.configure(image=img2)
            l_pic.image = img2


        if times%2 == 1:
            listButtons[x][y]["text"]="○"
            board[x][y] = "W"
            l_turn["text"]="Black, your turn!"
            img1 = ImageTk.PhotoImage(Image.open("Octocorn_Black.png"))
            l_pic.configure(image=img1)
            l_pic.image = img1

        times += 1

    #check if a player wins
    check_win(board)

    #if there is a winner, change the image label, the color of undo button
    if win=="black":
        #change the image
        img3 = ImageTk.PhotoImage(Image.open("Octocron_Black_Win.png"))
        l_pic.configure(image=img3)
        l_pic.image = img3
        #change the color of text in the undo button
        button_undo["fg"]="grey"
    if win=="white":
        img4 = ImageTk.PhotoImage(Image.open("Octocorn_White_Win.png"))
        l_pic.configure(image=img4)
        l_pic.image = img4
        button_undo["fg"] = "grey"


#undo button
def button_undo():
    """delete the move the latest player make"""
    global times
    global listButtons
    global board
    global row
    global col
    global l_pic
    global l_turn
    global button_undo

    #run the function only when there is a stone in that button and noone wins
    if listButtons[row][col]["text"]!="" and win=="":
        #change the text of button
        listButtons[row][col]["text"]=""
        #change the text in the board
        board[row][col]="O"

        #reset the interface to the former appearance
        times-=1

        if times%2==1:
            l_turn["text"]="White, Your turn!"
            img2 = ImageTk.PhotoImage(Image.open("Octocorn_White.png"))
            l_pic.configure(image=img2)
            l_pic.image = img2
        if times%2==0:
            l_turn["text"]="Black, Your turn!"
            img1 = ImageTk.PhotoImage(Image.open("Octocorn_Black.png"))
            l_pic.configure(image=img1)
            l_pic.image = img1


#new button
def button_new():
    """renew the entire window and the board"""
    global times
    global listButtons
    global board
    global l_turn
    global l_pic
    global win
    global button_undo

    win = ""
    times=0
    l_turn["text"]="Black, your turn!"

    for x in range(15):
        for y in range(15):
            board[x][y]="O"

    for x in listButtons:
        for y in x:
            y["text"] = ""
            y["fg"] = "black"

    l_turn["text"] = "Black, Your turn!"
    img1 = ImageTk.PhotoImage(Image.open("Octocorn_Black.png"))
    l_pic.configure(image=img1)
    l_pic.image = img1

    button_undo["fg"] = "black"



# ------------ script elements ---------- #


friendGUI()

