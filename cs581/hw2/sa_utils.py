import numpy as np

# Search Node

class Node:

    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent

    def __repr__(self):
        return "Node: {}".format(self.state)

    def path(self):
        current = self
        path_back = [current]
        while current.parent is not None:
            path_back.append(current.parent)
            current = current.parent

        return reversed(path_back)

    def expand(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError


# Algorithms

## Hill Climbing

def hill_climbing(initial_n):
    current_n = initial_n
    current_best = initial_n.value()

    while True:
        next_nodes = current_n.expand()
        next_vals = [node.value() for node in next_nodes]
        max_index = np.argmax(next_vals)
        if next_vals[max_index] > current_best:
            current_best = next_vals[max_index]
            current_n = next_nodes[max_index]
        else:
            return current_n


## Simulated Annealing

def simulated_annealing(initial_n, temp_schedule, max_iter, random_seed=0):

    rng = np.random.default_rng(seed=random_seed)
    
    current_n = initial_n

    best_n = initial_n
    
    for t in range(max_iter):

        T = temp_schedule(t)

        next_nodes = current_n.expand()

        if len(next_nodes) == 0:
            return current_n
        else:
            next_n = rng.choice(next_nodes)

            if next_n.value() > best_n.value():
                best_n = next_n

            delta_e =  next_n.value() - current_n.value()

            if delta_e > 0:
                current_n = next_n
            else:
                p = np.exp(delta_e/T)
                if rng.random() < p:
                    current_n = next_n
    return current_n, best_n


### Temperature Schedules for SA

#### Exponential schedule

def exp_schedule(k, lam):
    """One possible schedule function for simulated annealing"""
    return lambda t: k * np.exp(-lam * t)
