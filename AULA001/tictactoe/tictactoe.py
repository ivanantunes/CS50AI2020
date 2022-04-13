"""
Tic Tac Toe Player
"""

from copy import deepcopy
import math

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

    for i in range(3):
        plays = ""
        for j in range(3):
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


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    operation = None
    a = -math.inf
    b = math.inf

    if player(board) == X:
        if board == initial_state():
            return (0, 0)
        
        v = -math.inf
        for action in actions(board):
            r = minV(result(board, action), a, b)
            a = max(a, r)

            if r > v:
                v = r
                operation = action
    else:
        v = math.inf
        for action in actions(board):
            r = maxV(result(board, action), a, b)
            b = min(b, r)

            if r < v:
                v = r
                operation = action
    return operation

def maxV(board, a, b):

    v = -math.inf

    for action in actions(board):
        v = max(v, minV(result(board, action), a, b))
        a = max(a, v)
        if b <= a:
            break
    return v

def minV(board, a, b):

    v = math.inf

    for action in actions(board):
        v = min(v, maxV(result(board, action), a, b))
        b = min(b, v)
        if b <= a:
            break
    return v