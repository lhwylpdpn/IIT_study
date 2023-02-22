from mcts_search import mcts
import numpy as np
from operator import itemgetter
import pydot

def ucb1(mcnode, C = 1.4, alpha = 1):
    return (mcnode.U/(mcnode.N+alpha)) + \
    C * np.sqrt(np.log(mcnode.parent.N+alpha)/(mcnode.N+alpha))

def mcts_move(root_mcnode):
    best_mcnode = max([(child, child.N) for child in root_mcnode.children], key=itemgetter(1))[0]
    print("{}/{} = {:.2f}".format(best_mcnode.U, best_mcnode.N, best_mcnode.U/best_mcnode.N))
    return best_mcnode.gn.last_move()

def mcts_player(gn, util_f, seed = 0, max_iter=100):
    root_mcnode = mcts(gn, util_f, seed = seed, max_iter = max_iter)
    return mcts_move(root_mcnode)

# Visualization

def dot_graph(mc_root, max_nodes = None, min_N = None):
    frontier = [mc_root]

    graph = pydot.Dot("my_graph", graph_type="graph")

    nodes = 0

    while len(frontier) > 0:

        node = frontier.pop(0)


        graph.add_node(pydot.Node(str(id(node)), label=str(node)))

        if node.parent is not None:
            graph.add_edge(pydot.Edge(str(id(node.parent)), str(id(node))))

        if node.children is not None:

            if min_N is not None:
                for child in node.children:                
                    if child.N >= min_N:
                        frontier.append(child)
            else:
                frontier.extend(node.children)
        
        nodes += 1

        if max_nodes is not None:
            if nodes >= max_nodes:
                break

    return graph


def dot_graph_path(mc_root):
    frontier = [mc_root]

    graph = pydot.Dot("my_graph", graph_type="graph")

    while len(frontier) > 0:

        node = frontier.pop(0)


        graph.add_node(pydot.Node(str(id(node)), label=str(node)))

        if node.parent is not None:
            graph.add_edge(pydot.Edge(str(id(node.parent)), str(id(node))))

        if node.children is not None:
            best_mcnode = max([(child, child.N) for child in node.children], key=itemgetter(1))[0]
            frontier.append(best_mcnode)

    return graph