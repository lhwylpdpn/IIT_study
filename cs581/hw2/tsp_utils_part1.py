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
        res=f.readlines()
        start_line=0
        #print('test')
        for i in range(start_line,len(res)):
            if res[i].startswith("EOF"):
                break
            try:
                name, x, y = res[i].split()
                cities[name] = City(name, float(x), float(y))
            except:
                continue
    return cities

def subsample_cities(cities, number_of_cities, random_seed):
    rng = np.random.default_rng(random_seed)
    chosen_cities = rng.permutation(sorted(list(cities.keys())))

    chosen_cities = chosen_cities[:number_of_cities]
    chosen_cities = {k: cities[k] for k in chosen_cities}

    return chosen_cities

class TSPNode(Node):

    _cities = None

    def __init__(self, state, parent = None):
        super().__init__(state, parent)
    
    def __repr__(self):
        return "TSPNode: {}".format("-".join(self.state))

    def expand(self):

        children = []
        this_state=self.state.copy()
        #swap two cities
        for i in range(len(this_state)):
            tmp=this_state.copy()
            if i==len(this_state)-1:
                tmp[0], tmp[-1] = tmp[-1], tmp[0]
            else:
                tmp[i],tmp[i+1]=tmp[i+1],tmp[i]
            children.append(TSPNode(tmp,self))
        self.state=this_state


        
        return children
    
    def value(self):

        cost = 0
        #print(self.state)
        #计算当前state的每两个城市之间的距离之和
        for i in range(len(self.state)):
            if i==len(self.state)-1:
                cost+=np.sqrt((self._cities[self.state[0]].x-self._cities[self.state[-1]].x)**2+(self._cities[self.state[0]].y-self._cities[self.state[-1]].y)**2)
            else:
                cost+=np.sqrt((self._cities[self.state[i]].x-self._cities[self.state[i+1]].x)**2+(self._cities[self.state[i]].y-self._cities[self.state[i+1]].y)**2)

        return -1*cost


def create_initial_node(cities, random_seed):
    rng = np.random.default_rng(random_seed)
    initial_state = rng.permutation(list(cities.keys()))
    return TSPNode(initial_state)


def plot_cities(ax, cities, state):

    x = [cities[i].x for i in state]
    y = [cities[i].y for i in state]
    ax.scatter(x, y)
    for i in range(len(state)):
        ax.annotate(state[i], (x[i], y[i]))

def plot_path(ax, cities, state):
    x = [cities[i].x for i in state]
    y = [cities[i].y for i in state]
    x+=x[0:1]
    y+=y[0:1]
    ax.plot(x,y, 'r')

def compare_sols(sols, cities):
    _, axs = plt.subplots(1, len(sols), figsize=(len(sols)*10, 10))

    for i in range(len(sols)):
        plot_cities(axs[i], cities, sols[i][1].state)
        plot_path(axs[i], cities, sols[i][1].state)
        axs[i].set_title("{:}\n{:}\nCost: {:.2f}".format(sols[i][0], "-".join(sols[i][1].state), -1*sols[i][1].value()))

