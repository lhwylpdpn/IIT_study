"""
    Much of the code is inspired by https://github.com/aimacode/aima-python/
"""

import numpy as np


def minimax_decision(game_node):

    next_p = game_node.next_player()

    def max_value(gn):
        if gn.is_terminal():
            return gn.utility(next_p)
        v = -np.inf
        for move in gn.available_moves():
            v = max(v, min_value(gn.next_game_node(move)))
        return v

    def min_value(gn):
        if gn.is_terminal():
            return gn.utility(next_p)
        v = np.inf
        for move in gn.available_moves():
            v = min(v, max_value(gn.next_game_node(move)))
        return v

    moves = game_node.available_moves()

    return [(move, min_value(game_node.next_game_node(move))) for move in moves]

def alpha_beta_search(game_node):

    next_p = game_node.next_player()

    def max_value(gn, alpha, beta):
        if gn.is_terminal():
            return gn.utility(next_p)
        v = -np.inf
        for move in gn.available_moves():
            v = max(v, min_value(gn.next_game_node(move), alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(gn, alpha, beta):
        if gn.is_terminal():
            return gn.utility(next_p)
        v = np.inf
        for move in gn.available_moves():
            v = min(v, max_value(gn.next_game_node(move), alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alpha_beta_search:

    moves = game_node.available_moves()

    alpha = -np.inf
    beta = np.inf

    return [(move, min_value(game_node.next_game_node(move), alpha, beta)) for move in moves]
