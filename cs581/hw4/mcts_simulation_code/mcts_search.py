import numpy as np
import random

class MCNode:

    def __init__(self, gn, N = 0, U = 0, parent = None, children = None) -> None:
        self.gn = gn
        self.N = N
        self.U = U
        self.parent = parent
        self.children = children

        if parent is not None:
            self._depth = parent._depth + 1
        else:
            self._depth = 0

    def __repr__(self):
        return str(self.gn) + "\n" + "U/N: {}/{}".format(self.U, self.N)


def mcts(root_gn, util_func, seed=0, max_iter=100):

    def select_leaf(mcnode, util_f):
        if mcnode.children is not None:
            max_util = -np.inf
            chosen_child = None
            for child in mcnode.children:
                child_util = util_f(child)
                if child_util > max_util:
                    max_util = child_util
                    chosen_child = child
            return select_leaf(chosen_child, util_f)
        else:
            return mcnode

    def expand(mcnode, rg):
        if mcnode.gn.is_terminal():
            return mcnode
        else:
            moves = mcnode.gn.available_moves()
            child_mcnodes = []
            for move in moves:
                next_gn = mcnode.gn.next_game_node(move)
                child_mcnode = MCNode(next_gn, parent = mcnode)
                child_mcnodes.append(child_mcnode)
            mcnode.children = child_mcnodes

            return rg.choice(child_mcnodes)

    def simulate(mcnode, rg):

        current_gn = mcnode.gn
        while not current_gn.is_terminal():
            moves = current_gn.available_moves()
            move = rg.choice(moves)
            current_gn = current_gn.next_game_node(move)

        return current_gn.utility('X') # Util is from X's perspective

    def backprop(mcnode, util):

        current_mcnode = mcnode

        while current_mcnode is not None:

            current_mcnode.N += 1

            if current_mcnode.gn.last_played() == 'X': # Util is from X's perspective.
                current_mcnode.U += util
            else:
                current_mcnode.U += (1-util) # Assumes utils are between 0 and 1 and symmetric

            current_mcnode = current_mcnode.parent

    root_mcnode = MCNode(root_gn)

    rg = random.Random(seed)

    for _ in range(max_iter):
        leaf_mcnode = select_leaf(root_mcnode, util_func)
        child_mcnode = expand(leaf_mcnode, rg)
        util = simulate(child_mcnode, rg)
        backprop(child_mcnode, util)

    return root_mcnode


