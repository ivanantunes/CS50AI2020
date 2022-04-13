"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math
import random

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

    if board == initial_state():
        return X

    counterX = 0
    counterO = 0

    for row in board:
        counterX += row.count(X)
        counterO += row.count(O)

    if counterX > counterO:
        return O

    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    acts = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                acts.add((i, j))
    return acts


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i = action[0]
    j = action[1]

    boardCopy = deepcopy(board)

    if boardCopy[i][j] is EMPTY:
        boardCopy[i][j] = player(board)

    return boardCopy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in board:
        if row.count(X) == 3:
            return X

        if row.count(O) == 3:
            return O

    for j in range(3):
        plays = ""
        for i in range(3):
            plays += str(board[i][j])

        if plays == 'XXX':
            return X
        if plays == 'OOO':
            return O
    dig1 = ""
    dig2 = ""
    j = 2

    for i in range(3):
        dig1 += str(board[i][i])
        dig2 += str(board[i][j])
        j -= 1

    if dig1 == 'XXX' or dig2 == 'XXX':
        return X

    if dig1 == 'OOO' or dig2 == 'OOO':
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) or not actions(board):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    win = winner(board)

    if win is X:
        return 1
    elif win is O:
        return -1
    return 0

actions_explored = 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    'X' Player is trying to maximise the score, 'O' Player is trying to minimise it
    """

    global actions_explored
    actions_explored = 0

    def maxValue(board, best_min=10):

        global actions_explored

        if terminal(board):
            return (utility(board), None)

        value = -10
        best_action = None

        actionS = actions(board)

        while len(actionS) > 0:
            action = random.choice(tuple(actionS))
            actionS.remove(action)

            if best_min <= value:
                break

            actions_explored += 1
            minValue_result = minValue(result(board, action), value)
            if minValue_result[0] > value:
                best_action = action
                value = minValue_result[0]

        return (value, best_action)

    def minValue(board, best_max=-10):

        global actions_explored

        if terminal(board):
            return (utility(board), None)

        value = 10
        best_action = None

        action_set = actions(board)

        while len(action_set) > 0:
            action = random.choice(tuple(action_set))
            action_set.remove(action)

            if best_max >= value:
                break

            actions_explored += 1
            maxValue_result = maxValue(result(board, action), value)
            if maxValue_result[0] < value:
                best_action = action
                value = maxValue_result[0]

        return (value, best_action)

    if terminal(board):
        return None

    if player(board) == 'X':
        best_move = maxValue(board)[1]
        return best_move
    else:
        best_move = minValue(board)[1]
        return best_move
