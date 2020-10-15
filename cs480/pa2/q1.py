import sys
from collections import namedtuple
from typing import Dict, Tuple

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


def file_read(filename):
    board: Dict[Tuple[int, int], str] = {}
    i = 0
    with open(filename, 'r', encoding='utf-8') as f:
        res = f.readlines()
    for r in res:
        if len(r) > 0:
            r = r.replace('\n', '').split(' ')
            for j in range(0, len(r)):
                board[i+1, j+1] = r[j].upper()
            i += 1

    return board


class game_problem():

    def __init__(self, _players, init_board={},h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        self.players = [r for r in _players]
        moves = [(x, y) for x in range(1, h + 1) for y in range(1, v + 1)]

        for k in init_board.keys():

            if init_board[k].upper()=='X' or init_board[k].upper()=='O':
                moves.remove(k)

        self.initial = GameState(to_move='', utility=0, board=init_board, moves=moves)
        self.initial = GameState(to_move=self.to_move(self.initial), utility=0, board=init_board, moves=moves)



    def to_move(self, state):
        res = {"X": 0, "O": 0}
        for p in state.board.values():
            if p.upper() == "X":
                res['X'] += 1
            if p.upper() == "O":
                res['O'] += 1
        return 'X' if res["X"] >= res["O"] else 'O'

    def actions(self, state):

        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves)

    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility

    def Terminal_test(self, state):
        return state.utility != 0 or len(state.moves) == 0

    def compute_utility(self, board, move, player):

        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'X' else -1
        else:
            return 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), '.'), end=' ')
            print()

    def k_in_row(self, board, move, player, delta_x_y):
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0
        while board.get((x, y)) == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while board.get((x, y)) == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1
        return n >= self.k


def alpha_beta_search(state, game):
    player = game.to_move(state)

    # Functions used by alpha_beta
    def max_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:
    best_score = -np.inf
    beta = np.inf
    best_action = None
    for a in game.actions(state):
        v = min_value(game.result(state, a), best_score, beta)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action


def minmax_decision(state, game):
    player = game.to_move(state)

    def max_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = -np.inf
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        return v

    def min_value(state):
        if game.terminal_test(state):
            return game.utility(state, player)
        v = np.inf
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        return v

    return max(game.actions(state), key=lambda a: min_value(game.result(state, a)))


if __name__ == '__main__':
    input_file = sys.argv[1]

    # TODO implement
    game = game_problem(['X', 'O'],file_read(input_file))
    # minmax_decision(,game)

    print('Whose turn is it in this state?')
    # TODO: print either X or O
    print(
        'If both X and O play optimally from this state, does X have a guaranteed win, guaranteed loss, or guaranteed draw')
# TODO: print one of win, loss, draw
