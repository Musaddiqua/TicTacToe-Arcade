import tkinter as tk
from tkinter import messagebox

def analyseboard(board):
    c = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for i in range(0, 8):
        if (board[c[i][0]] != 0 and
            board[c[i][0]] == board[c[i][1]] and
            board[c[i][1]] == board[c[i][2]]):
            return board[c[i][0]]
    return 0

def constBoard(board, buttons):
    for i in range(9):
        if board[i] == 0:
            buttons[i].config(text=" ", bg="black")
        elif board[i] == 1:
            buttons[i].config(text="O", fg="blue", font=('Helvetica', 40, 'bold'))
        elif board[i] == -1:
            buttons[i].config(text="X", fg="red", font=('Helvetica', 40, 'bold'))

def userTurn(board, buttons, pos, player):
    if board[pos] != 0:
        messagebox.showerror("Error", "Invalid move! Try again.")
        return False
    board[pos] = player
    constBoard(board, buttons)
    return True

def minmax(board, player):
    winner = analyseboard(board)
    if winner != 0:
        return winner * player
    pos = -1
    value = -2
    for i in range(9):
        if board[i] == 0:
            board[i] = player
            score = -minmax(board, -player)
            board[i] = 0
            if score > value:
                value = score
                pos = i
    if pos == -1:
        return 0
    return value

def compTurn(board, buttons):
    pos = -1
    value = -2
    for i in range(9):
        if board[i] == 0:
            board[i] = 1
            score = -minmax(board, -1)
            board[i] = 0
            if score > value:
                value = score
                pos = i
    board[pos] = 1
    constBoard(board, buttons)

def checkGameState(board, buttons, player):
    winner = analyseboard(board)
    if winner != 0:
        if winner == 1:
            messagebox.showinfo("Game Over", "Player 2 (O) has won!")
        else:
            messagebox.showinfo("Game Over", "Player 1 (X) has won!")
        resetBoard(board, buttons)
        return True
    elif 0 not in board:
        messagebox.showinfo("Game Over", "It's a draw!")
        resetBoard(board, buttons)
        return True
    return False

def resetBoard(board, buttons):
    for i in range(9):
        board[i] = 0
    constBoard(board, buttons)

def main():
    board = [0] * 9
    player = -1  # Player 1 starts first (X)

    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    # Set up the frame with a dark background to make it look more like a gaming board
    frame = tk.Frame(root, bg="black")
    frame.pack()

    buttons = []
    for i in range(9):
        button = tk.Button(frame, text=" ", font=('Helvetica', 40, 'bold'), width=5, height=2, bg="black", fg="white",
                           command=lambda i=i: onButtonClick(i, board, buttons, player))
        button.grid(row=i//3, column=i%3)
        buttons.append(button)

    def onButtonClick(i, board, buttons, player):
        if userTurn(board, buttons, i, player):
            if not checkGameState(board, buttons, player):
                compTurn(board, buttons)
                checkGameState(board, buttons, player)

    reset_button = tk.Button(root, text="Reset", font=('Helvetica', 20), command=lambda: resetBoard(board, buttons))
    reset_button.pack(side="bottom")

    root.mainloop()

if __name__ == "__main__":
    main()
