import random


def check_next_move(cells, board):

    for empty_cell in cells:
        r, c = empty_cell
        board[r][c] = 'O'
        if check_winner(board):
            board[r][c] = ''
            return empty_cell
        board[r][c] = ''

    for empty_cell in cells:
        r, c = empty_cell
        board[r][c] = 'X'
        if check_winner(board):
            board[r][c] = ''
            return empty_cell
        board[r][c] = ''

    return random.choice(cells)


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


def get_bot_move(board, board_s, difficulty):
    empty_cells = [(r, c) for r in range(board_s) for c in range(board_s) if board[r][c] == '']

    if not empty_cells:
        return None

    if difficulty == 'Easy':
        return random.choice(empty_cells)

    elif difficulty == 'Hard':
        return check_next_move(empty_cells, board)

    elif difficulty == 'Unbeatable':
        score = float('-inf')
        cords = (0, 0)

        for cell in empty_cells:
            r, c = cell
            board[r][c] = 'O'
            current_score = minimax(board, is_maximazing=False)
            board[r][c] = ''
            if score < current_score:
                score = current_score
                cords = r, c

        return cords

    return random.choice(empty_cells)


def minimax(board, is_maximazing):
    win = 10
    draw = 0


    if check_winner(board):
        return -win if is_maximazing else win
    if is_draw(board):
        return draw

    empty_cells = [(r, c) for r in range(len(board)) for c in range(len(board)) if board[r][c] == '']
    if is_maximazing:
        best_score = float('-inf')

        for cell in empty_cells:
            r, c = cell
            board[r][c] = 'O'
            score = minimax(board, is_maximazing=False)
            board[r][c] = ''
            if best_score < score:
                best_score = score

        return best_score

    else:
        best_score = float('inf')

        for cell in empty_cells:
            r, c = cell
            board[r][c] = 'X'
            score = minimax(board, is_maximazing=True)
            board[r][c] = ''
            if best_score > score:
                best_score = score

        return best_score


def update_score(current_score):
    return current_score + 1