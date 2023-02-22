import numpy as np
import random

class MCNode:

    def __init__(self, gn, N = 0, U = 0, parent = None, children = None) -> None:
        self.gn = gn
        self.N = N
        self.U = U
        self.parent = parent
        self.children = children

    def __repr__(self):
        return str(self.gn) + "\n" + "U/N: {}/{}".format(self.U, self.N)


def mcts(root_gn, util_func, seed=0, max_iter=100):

    def select_leaf(mcnode, util_f):
        '''Choose a leaf node. For every non-leaf node,
        choose its max util (as defined by util_f) child node.
        Return an MCNode object.'''
        raise NotImplementedError

    def expand(mcnode, rg):
        '''Given a leaf node, if its a terminal node, return it.
        Otherwise, create all of its children and return one at random.'''
        raise NotImplementedError

    def simulate(mcnode, rg):
        '''Starting from mcnode, choose moves at random until the terminal node.
        Return the utility of the terminal node from the perspective of X.'''
        raise NotImplementedError

    def backprop(mcnode, util):
        '''Backprob the simulation to the ancestor nodes.
        Increment N for all ancestor nodes. Update the util for the correct side.'''
        raise NotImplementedError
    
    # Body of the search
    root_mcnode = MCNode(root_gn)
    rg = random.Random(seed)

    for _ in range(max_iter):
        leaf_mcnode = select_leaf(root_mcnode, util_func)
        child_mcnode = expand(leaf_mcnode, rg)
        util = simulate(child_mcnode, rg)
        backprop(child_mcnode, util)

    return root_mcnode


