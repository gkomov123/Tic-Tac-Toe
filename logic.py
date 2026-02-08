import random


def check_winner(board):
    for i in range(len(board)):
        # Row check: Are all items in board[i] the same
        if all(cell == board[i][0] != '' for cell in board[i]):
            return True

        # Column check: Are all items in column i the same
        column = [board[r][i] for r in range(len(board))]
        if all(cell == column[0] != '' for cell in column):
            return True

    # Check diagonals
    main_diag = [board[i][i] for i in range(len(board))]
    if all(cell == main_diag[0] != '' for cell in main_diag):
        return True

    anti_diag = [board[i][len(board) - 1 - i] for i in range(len(board))]
    if all(cell == anti_diag[0] != '' for cell in anti_diag):
        return True

    return False


def toggle_player(c_player):
    return 'O' if c_player == 'X' else 'X'


def is_draw(board):
    # Returns True if no empty strings are left in the matrix
    return all('' not in row for row in board)


def create_board(board_s):
    matrix = [["" for _ in range(board_s)] for _ in range(board_s)]
    return matrix


def get_bot_move(board):
    empty_cells = [(r ,c) for r in range(3) for c in range(3) if board[r][c] == '']
    return random.choice(empty_cells) if empty_cells else None


def update_score(current_score):
    return current_score + 1