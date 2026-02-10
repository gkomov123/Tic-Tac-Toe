import tkinter as tk
from tkinter import messagebox

from logic import check_winner, toggle_player, is_draw, get_bot_move, create_board, update_score


def toggle_mode():
    global game_mode_bot, mode_btn_text

    game_mode_bot = not game_mode_bot
    if game_mode_bot:
        mode_btn_text.set('Player vs AI')
    else:
        mode_btn_text.set('Player vs Player')


def clear_game_state():
    global GAME_OVER, current_player, bot_thinking, bot_job

    if bot_job:
        root.after_cancel(bot_job)
        bot_job = None

    GAME_OVER = False
    bot_thinking = False
    current_player = 'X'



def reset_current_game():
    global GAME_OVER, current_player, bot_thinking, bot_job

    # Remove old game frame
    game_frame.destroy()

    # Reset logic in logic.py
    global matrix
    matrix = create_board(BOARD_SIZE)

    # Build new GUI grid
    create_board_gui(BOARD_SIZE)

    clear_game_state()

def trigger_bot_move():
    global current_player, bot_thinking

    move = get_bot_move(matrix, BOARD_SIZE)
    if move:
        bot_row, bot_col = move
        bot_ended = make_move(bot_row, bot_col)

        if not bot_ended:
            current_player = toggle_player(current_player)
            bot_thinking = False


def make_move(row, col):
    global current_player, GAME_OVER, score_x_count, score_o_count, score_x_var, score_o_var, bot_thinking

    # 1. Update the logic board (matrix)
    matrix[row][col] = current_player

    # 2. Update the GUI button
    color = 'red' if current_player == 'X' else 'blue'
    buttons[row][col].config(text=current_player, fg=color)

    # 3. Check for Win/Tie
    if check_winner(matrix):
        messagebox.showinfo("Game Over", f"Player {current_player} wins! 🎉")
        GAME_OVER = True
        bot_thinking = False

        if current_player == 'X':
            score_x_count = update_score(score_x_count)
            score_x_var.set(f"Player X: {score_x_count}")
        else:
            score_o_count = update_score(score_o_count)
            score_o_var.set(f"Player O: {score_o_count}")

        return True

    if is_draw(matrix):
        messagebox.showinfo("Game Over", "It's a tie! 🤝")
        bot_thinking = False
        GAME_OVER = True

        return True

    return False # Game continues


def handle_click(row, col):
    global current_player, GAME_OVER, bot_job, bot_thinking, game_mode_bot

    if GAME_OVER or matrix[row][col] != '' or bot_thinking:
        return

    # Human turn
    ended = make_move(row, col)

    # Switch player
    current_player = toggle_player(current_player)

    if not ended and game_mode_bot:

        # We use the root window to schedule the delay
        bot_thinking = True
        bot_job = root.after(500 , trigger_bot_move)


def show_menu():
    global menu_frame, size_var, game_mode_bot, mode_btn_text

    # Create container for the menu
    menu_frame = tk.Frame(root)
    menu_frame.pack(pady=20)

    tk.Label(menu_frame, text='Tic Tac Toe Settings', font=('Helvetica', 24)).pack(pady=10)

    # Number box for board size
    tk.Label(menu_frame, text='Choose Board Size (3-10):').pack()
    size_var = tk.IntVar(value=3) # Default 3
    spin = tk.Spinbox(menu_frame, from_=3, to=10, textvariable=size_var, width=5)
    spin.pack(pady=10)

    # Start button
    start_btn = tk.Button(menu_frame, text='Start Game', command=start_game)
    start_btn.pack(pady=20)


    # Game mode button
    mode_btn_text = tk.StringVar(value='Player vs AI' if game_mode_bot else 'Player vs Player')
    mode_btn = tk.Button(menu_frame, textvariable=mode_btn_text, command=toggle_mode)
    mode_btn.pack(pady=20)


    # Bot Level selection menu
    difficulty_options = ['Easy', 'Hard', 'Unbeatable']
    bot_difficulty = tk.StringVar(value='Easy')

    dropdown = tk.OptionMenu(menu_frame, bot_difficulty, *difficulty_options)
    dropdown.pack(pady=20)

def back_to_settings():

    # Hide game frame
    game_frame.destroy()

    # Show settings menu
    menu_frame.pack(pady=20)

    clear_game_state()

def start_game():
    global BOARD_SIZE, matrix

    # Hide Menu
    menu_frame.pack_forget()

    # Get board size
    BOARD_SIZE = size_var.get()

    # Create logic matrix
    matrix = create_board(BOARD_SIZE)

    # Draw grid
    create_board_gui(BOARD_SIZE)


def create_board_gui(size):
    global game_frame, buttons, score_frame

    # Clear the window of any existing game widgets
    for widget in root.winfo_children():
        if widget != menu_frame and widget != score_frame:
            widget.destroy()


    game_frame = tk.Frame(root)
    game_frame.pack(expand=True, fill="both")

    control_frame = tk.Frame(game_frame)
    control_frame.grid(row=size, column=0, columnspan=size, sticky='we')


    dynamic_font = ('Helvetica', int(100 / size), 'bold')

    # 1. Configure the internal grid of game_frame to be stable
    for i in range(size):
        game_frame.grid_rowconfigure(i, weight=1, uniform="square_grid")
        game_frame.grid_columnconfigure(i, weight=1, uniform="square_grid")

    buttons = []
    for r in range(size):
        row_buttons = []
        for c in range(size):
            btn = tk.Button(
                game_frame,
                text='',
                font=dynamic_font,
                width=3,
                height=1,
                command=lambda row=r, col=c: handle_click(row, col)
            )
            btn.grid(row=r, column=c, sticky='nsew')
            row_buttons.append(btn)
        buttons.append(row_buttons)

    # Reset button
    reset_btn = tk.Button(control_frame, text="Reset", command=reset_current_game)
    reset_btn.pack(side='left', expand=True, fill='x')

    # Settings Button (Goes back to the menu)
    settings_btn = tk.Button(control_frame, text="Settings", command=back_to_settings)
    settings_btn.pack(side='right', expand=True, fill='x')


    # Configure grid to be flexible
    for i in range(size):
        root.grid_rowconfigure(i + 1, weight=1, uniform='group1') # +1 because row 0 is for the score
        root.grid_columnconfigure(i, weight=1, uniform='group1')


def setup_scoreboard():
    global score_x_var, score_o_var, score_frame

    score_frame = tk.Frame(root, bg='lightgrey', pady=10)
    score_frame.pack(fill='x')

    score_x_var = tk.StringVar(value='Player X: 0')
    score_o_var = tk.StringVar(value='Player O: 0')

    tk.Label(score_frame, textvariable=score_x_var, font=("Helvetica", 14)).pack(side='left', padx=20)
    tk.Label(score_frame, textvariable=score_o_var, font=("Helvetica", 14)).pack(side='right', padx=20)


# Global State 🌍
BOARD_SIZE = 3
GAME_OVER = False
current_player = "X"
matrix = create_board(BOARD_SIZE)
buttons = []
score_x_count = 0
score_o_count = 0
score_x_var = None
score_o_var = None
bot_job = None
menu_frame = None
game_frame = None
score_frame = None
size_var = 3
bot_thinking = False
game_mode_bot = True
mode_btn_text = None


root = tk.Tk()
root.title('Tic Tac Toe')

setup_scoreboard()
show_menu()

root.mainloop()