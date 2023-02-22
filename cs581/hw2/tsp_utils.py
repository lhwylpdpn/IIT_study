import numpy as np
import matplotlib.pyplot as plt

from sa_utils import Node

class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "City: {} ({:.2f} {:.2f})".format(self.name, self.x, self.y)

def read_cities(tsp_file):
    
    cities = {}
    
    with open(tsp_file, 'r') as f:

        line = ""

        while line != "NODE_COORD_SECTION\n":
            line = f.readline()

        for line in f:
            if line == "EOF\n":
                break
            else:
                city_info = line.split()
                cities[city_info[0]] = City(city_info[0], float(city_info[1]), float(city_info[2]))
    
    return cities   

def subsample_cities(cities, number_of_cities, random_seed):
    rng = np.random.default_rng(random_seed)
    chosen_cities = rng.permutation(sorted(list(cities.keys())))
    sample_cities = {}
    for k in chosen_cities[:number_of_cities]:
        sample_cities[k] = cities[k]
    
    return sample_cities

class TSPNode(Node):

    _cities = None

    def __init__(self, state, parent = None):
        super().__init__(state, parent)
    
    def __repr__(self):
        return "TSPNode: {}".format("-".join(self.state))

    def expand(self):

        children = []

        for i in range(len(self.state)):
            
            new_state = self.state.copy()
            
            new_state[i] = self.state[(i+1) % len(self.state)]
            new_state[(i+1) % len(self.state)] = self.state[i]
            
            children.append(TSPNode(new_state, self))
        
        return children

    def _distance(a, b):
        city_a = TSPNode._cities[a]
        city_b = TSPNode._cities[b]
        return np.sqrt ((city_a.x - city_b.x)**2 + (city_a.y - city_b.y)**2)
    
    def value(self):
        
        cost = 0
        
        for i in range(len(self.state)):
            
            cost += TSPNode._distance(self.state[i], self.state[(i+1) % len(self.state)])
        

        return -1*cost


def create_initial_node(cities, random_seed):
    rng = np.random.default_rng(random_seed)
    initial_state = rng.permutation(list(cities.keys()))
    return TSPNode(initial_state)


def plot_cities(ax, cities, state):
    for s in state:
        city = cities[s]
        ax.scatter(city.x, city.y, marker='x', c='r', s=100)
        ax.text(city.x, city.y+0.04, city.name, fontsize='large')

def plot_path(ax, cities, state):
    for i in range(len(state)):
        city_a = cities[state[i]]
        city_b = cities[state[(i+1)%len(state)]]
        begin = [city_a.x, city_b.x]
        end = [city_a.y, city_b.y]
        ax.plot(begin, end, 'k-', lw=2)

def compare_sols(sols, cities):
    _, axs = plt.subplots(1, len(sols), figsize=(len(sols)*10, 10))

    for i in range(len(sols)):
        plot_cities(axs[i], cities, sols[i][1].state)
        plot_path(axs[i], cities, sols[i][1].state)
        axs[i].set_title("{:}\n{:}\nCost: {:.2f}".format(sols[i][0], "-".join(sols[i][1].state), -1*sols[i][1].value()))


def visualize_solution_progression(cities, soln_order):
    
    def _find_edges(state):
        if state is None:
            return set()

        edges = set()
        for i in range(len(state)):
            edges.add((state[i], state[(i+1) % len(state)]))

        return edges
    
    fig, axs = plt.subplots(len(soln_order), 2, figsize=(10, 6*len(soln_order)))

    previous_state = None

    for i in range(len(soln_order)):

        plot_cities(axs[i][0], cities, soln_order[i].state)
        plot_cities(axs[i][1], cities, soln_order[i].state)

        current_state = soln_order[i].state

        previous_edges = _find_edges(previous_state)

        current_edges = _find_edges(current_state)

        common_edges = current_edges.intersection(previous_edges)
        ex_edges = previous_edges.difference(current_edges)
        new_edges = current_edges.difference(previous_edges)

        for edge in common_edges:
            city_a = cities[edge[0]]
            city_b = cities[edge[1]]
            begin = [city_a.x, city_b.x]
            end = [city_a.y, city_b.y]
            axs[i][0].plot(begin, end, 'k-', lw=2)
            axs[i][1].plot(begin, end, 'k-', lw=2)

        for edge in new_edges:
            city_a = cities[edge[0]]
            city_b = cities[edge[1]]
            begin = [city_a.x, city_b.x]
            end = [city_a.y, city_b.y]
            axs[i][1].plot(begin, end, 'b-', lw=2)

        for edge in ex_edges:
            city_a = cities[edge[0]]
            city_b = cities[edge[1]]
            begin = [city_a.x, city_b.x]
            end = [city_a.y, city_b.y]
            axs[i][0].plot(begin, end, 'g:', lw=2)
        if previous_state is not None:
            axs[i][0].set_title("Path: {:}\n".format("-".join(previous_state)))
        axs[i][1].set_title("Path: {:}\nCost {:.2f}".format("-".join(soln_order[i].state), -1*soln_order[i].value()))


        previous_state = current_state

