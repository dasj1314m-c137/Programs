"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    num_X = 0
    num_O = 0

    turn = None

    for lst in board:
        num_O += lst.count(O)
        num_X += lst.count(X)

    if num_X > num_O:
        turn = O
    elif num_X == num_O:
        turn = X

    return turn
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row, lst in enumerate(board):
        for column, cell in enumerate(lst):
            if cell == EMPTY:
                actions.add((row, column))
    return actions

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    row = action[0]
    column = action[1]

    if not 0 <= row < 3 or not 0 <= column < 3:
        raise ValueError("Invalid action")

    if new_board[row][column] != EMPTY:
        raise ValueError("Invalid action cell not empty")

    new_board[row][column] = player(board)

    return new_board
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_horizontal(board, player):
        for horizontal in board:
            if horizontal.count(player) == 3:
                return player
        return None

    def check_vertical(board, player):
        vertical = []
        for i in range(3):
            for j in range(3):
                vertical.append(board[j][i])
            if vertical.count(player) == 3:
                return player
            vertical.clear()
        return None

    def check_diagonal(board, player):
        diagonal = []
        for i in range(3):
            diagonal.append(board[i][i])
        if diagonal.count(player) == 3:
            return player
        diagonal.clear()
        diagonal.append(board[0][2])
        diagonal.append(board[1][1])
        diagonal.append(board[2][0])
        if diagonal.count(player) == 3:
            return player
        return None

    checks = [check_horizontal, check_vertical, check_diagonal]

    for player in [X, O]:
        for check in checks:
            result = check(board, player)
            if result is not None:
                return result
    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    result_winner = winner(board)
    if result_winner is not None:
        return True

    for row in board:
        if EMPTY in row:
            return False
    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result_winner = winner(board)
    if result_winner is not None:
        return 1 if result_winner == X else -1
    return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    terminal_board = terminal(board)
    if terminal_board:
        return None

    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    bst_move = None
    max_score = -math.inf
    min_score = math.inf

    if player(board) == X:
        for action in actions(board):
            new_board = result(board, action)
            if (current_score := min_value(new_board)) > max_score:
                bst_move = action
                max_score = current_score
    else:
        for action in actions(board):
            new_board = result(board, action)
            if (current_score := max_value(new_board)) < min_score:
                bst_move = action
                min_score = current_score

    return bst_move

    raise NotImplementedError


if __name__ == "__main__":
    testing_board = [
            [X, EMPTY, EMPTY],
            [EMPTY, O, O],
            [X, X, EMPTY]
            ]

    bst_move = minimax(testing_board)

    print(bst_move)
    pass