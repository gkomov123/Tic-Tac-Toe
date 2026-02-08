import tkinter as tk
from tkinter import messagebox
from logic import check_winner, toggle_player, is_draw, get_bot_move, create_board, update_score


def clear_board():
    global current_player, matrix, GAME_OVER, bot_job

    if bot_job:
        root.after_cancel(bot_job)
        bot_job = None

    current_player = 'X'
    GAME_OVER = False

    # Reset buttons
    for button_list in buttons:
        for butn in button_list:
            butn.config(text='', fg='black')

    # Reset logic board
    matrix = create_board(BOARD_SIZE)


def trigger_bot_move():
    global current_player

    move = get_bot_move(matrix)
    if move:
        bot_row, bot_col = move
        bot_ended = make_move(bot_row, bot_col)

        if not bot_ended:
            current_player = toggle_player(current_player)


def make_move(row, col):
    global current_player, GAME_OVER, score_x, score_o

    # 1. Update the logic board (matrix)
    matrix[row][col] = current_player

    # 2. Update the GUI button
    color = 'red' if current_player == 'X' else 'blue'
    buttons[row][col].config(text=current_player, fg=color)

    # 3. Check for Win/Tie using our logic.py functions
    if check_winner(matrix):
        messagebox.showinfo("Game Over", f"Player {current_player} wins! 🎉")
        GAME_OVER = True
        if current_player == 'X':
            score_x = update_score(score_x)
        else:
            score_o = update_score(score_o)
        score_label.config(text=f"X: {score_x} | O: {score_o}")

        return True # Return True if the game ended

    if is_draw(matrix):
        messagebox.showinfo("Game Over", "It's a tie! 🤝")
        GAME_OVER = True
        return True

    return False # Game continues


def handle_click(row, col):
    global current_player, GAME_OVER, bot_job

    if GAME_OVER or matrix[row][col] != '':
        return

    # Human turn
    ended = make_move(row, col)

    if not ended:
        # Switch to bot
        current_player = toggle_player(current_player)

        # We use the root window to schedule the delay
        bot_job = root.after(500 , trigger_bot_move)

# Global State 🌍
BOARD_SIZE = 3
GAME_OVER = False
current_player = "X"
matrix = create_board(BOARD_SIZE)
buttons = []
score_x = 0
score_o = 0
bot_job = None


root = tk.Tk()
root.title('Tic Tac Toe')


# Button and creation l ogic
for r in range(BOARD_SIZE):
    row_buttons = []
    for c in range(BOARD_SIZE):
        # Create button
        btn = tk.Button(
            root,
            text='',
            width=5,  # Adjusted width/height for larger font
            height=2,
            bg='white',
            font=("Helvetica", 24, "bold"),  # Large font for game pieces
            command=lambda row=r, col=c: handle_click(row, col)
        )
        # Place button
        btn.grid(row=r + 1, column=c)
        row_buttons.append(btn)
    buttons.append(row_buttons)

# Create reset button
reset_btn = tk.Button(
    root,
    text='RESET',
    width=5,
    height=2,
    bg='white',
    fg='black',
    font=("Helvetica", 14, "bold"),
    command=clear_board
    )
reset_btn.grid(row=4, column=0, columnspan=3, sticky='we')

# Score Board label
score_label = tk.Label(root, text=f"X: {score_x} | O: {score_o}", font=("Helvetica", 16, "bold"))
score_label.grid(row=0, column=0, columnspan=3)

root.mainloop()