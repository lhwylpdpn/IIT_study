from collections import defaultdict
from dataclasses import dataclass
from operator import itemgetter
from time import process_time

import numpy as np
from game_boards import ConnectFour, MNKNode

from game_play import maxplayer, randplayer
from game_search import alpha_beta_search
from mcts_search import MCNode, mcts
from mcts_utils import mcts_player, ucb1


@dataclass
class TreeStats:
    number_of_simulated_nodes: int
    max_tree_depth: int
    max_leaf_node: MCNode

def tree_stats(root_mc):

    frontier = [root_mc]

    number_of_simulated_nodes = 0
    max_tree_depth = 0

    while len(frontier) > 0:

        node = frontier.pop(0)

        if node._depth > max_tree_depth:
            max_tree_depth = node._depth

        if node.N > 0:
            number_of_simulated_nodes += 1

        if node.children is not None:
            frontier.extend(node.children)

    max_leaf_node = None
    frontier = [root_mc]
    while len(frontier) > 0:
        node = frontier.pop(0)
        if node.children is not None:
            best_mcnode = max([(child, child.N)
                              for child in node.children], key=itemgetter(1))[0]
            frontier.append(best_mcnode)
        else:
            max_leaf_node = node

    ts = TreeStats(number_of_simulated_nodes=number_of_simulated_nodes,
                   max_tree_depth=max_tree_depth, max_leaf_node=max_leaf_node)
    return ts

def average_branching_factor(number_of_nodes, depth):
    depth = int(depth)
    arr_for_np_roots = np.ones(depth+1)
    arr_for_np_roots[depth] = -number_of_nodes
    all_roots = np.roots(arr_for_np_roots)
    real_roots = all_roots[np.isreal(all_roots)]
    positive_real_roots = real_roots[real_roots > 0]
    return abs(positive_real_roots[0])

def create_empty_ttt():
    empty_board = []

    for _ in range(3):
        empty_board.append(['-', '-', '-'])

    return MNKNode(empty_board, k = 3)

def create_empty_c4():
    empty_board = []

    for _ in range(6):
        empty_board.append(['-', '-', '-', '-', '-', '-', '-'])

    return ConnectFour(empty_board)

def simulate_mcts(game, Cs, s, max_iters):

    if game == 'ttt':
        gn = create_empty_ttt()
    elif game == 'c4':
        gn = create_empty_c4()
    else:
        raise ValueError("Unknown game type", game)

    results = {}

    for c in Cs:
        util_f = lambda mcnode: ucb1(mcnode, C=c)
        results[c] = {}
        for max_iter in max_iters:
            ttt_root_mc = mcts(gn, util_func=util_f, seed = s, max_iter=max_iter)
            ts = tree_stats(ttt_root_mc)
            results[c][max_iter] = {}
            results[c][max_iter]['number_of_nodes']= ts.number_of_simulated_nodes
            results[c][max_iter]['max_depth'] = ts.max_tree_depth
            results[c][max_iter]['branching_factor'] = average_branching_factor(ts.number_of_simulated_nodes, ts.max_tree_depth)
            results[c][max_iter]['root_ave_util'] = ttt_root_mc.U/ttt_root_mc.N
            results[c][max_iter]['reached_terminal'] = ts.max_leaf_node.gn.is_terminal()

    return results

def play_one_full_game(gn, x_player, o_player):
    current_gn = gn
    x_running_time, o_running_time = 0, 0

    while not current_gn.is_terminal():
        p = current_gn.next_player()

        if p == 'X':
            x_start_time = process_time()
            chosen_move = x_player(current_gn)
            x_move_time = process_time() - x_start_time
            x_running_time += x_move_time
        else:
            o_start_time = process_time()
            chosen_move = o_player(current_gn)
            o_move_time = process_time() - o_start_time
            o_running_time += o_move_time

        current_gn = current_gn.next_game_node(chosen_move)


    winner = current_gn.winner()

    return winner, x_running_time, o_running_time

def simulate_mcts_gp(game, xp, op, Cs, s, max_iters, opponent_args=None):

    if game == 'ttt':
        gn = create_empty_ttt()
    elif game == 'c4':
        gn = create_empty_c4()
    else:
        raise ValueError("Unknown game type", game)

    gm_results = {}

    for c in Cs:
        util_f = lambda mcnode: ucb1(mcnode, C=c)
        gm_results[c] = {}
        for max_iter in max_iters:
            gm_results[c][max_iter] = defaultdict(list)

            x_player = None
            o_player = None

            def _get_player(p):
                if p == 'mcts':
                    return lambda b:  mcts_player(b, util_f, seed = s, max_iter=max_iter)
                elif p == 'random':
                    return lambda b: randplayer(b, seed=s)
                elif p == 'alpha_beta':
                    return lambda b: maxplayer(b, algo=alpha_beta_search)
                elif p == "mcts_base":
                    util_base = lambda mcnode: ucb1(mcnode, C=opponent_args['C'])
                    return lambda b:  mcts_player(b, util_base, seed = s, max_iter=opponent_args['max_iter'])
                else:
                    raise ValueError("iIvalid player", p)


            x_player = _get_player(xp)
            o_player = _get_player(op)

            winner, x_rt, o_rt = play_one_full_game(gn, x_player, o_player)

            gm_results[c][max_iter][xp+'_Win'] = (winner=='X')
            gm_results[c][max_iter][xp+'_Loss'] = (winner=='O')
            gm_results[c][max_iter]['Draw'] = (winner is None)
            gm_results[c][max_iter][xp+'_RunTime'] = x_rt
            gm_results[c][max_iter][op+'_RunTime'] = o_rt
    return gm_results
