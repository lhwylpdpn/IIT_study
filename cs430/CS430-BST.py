#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
from collections import Iterable


class Node:
    
    def __init__(self, value, left=None, right=None):
        self.value = value   # 节点的值
        self.left = left     # 左子节点
        self.right = right   # 右子节点

class BinaryTree:

    def __init__(self, seq=()):
        assert isinstance(seq, Iterable)  # 确保输入的参数为可迭代对象
        self.root = None 

    def insert(self, *args):
        if not args:
            return
        if not self.root:
            self.root = Node(args[0])
            args = args[1:]
        for i in args:
            seed = self.root
            while True:
                if i > seed.value:
                    if not seed.right:
                        node = Node(i)
                        seed.right = node
                        break
                    else:
                        seed = seed.right
                else:
                    if not seed.left:
                        node = Node(i)
                        seed.left = node
                        break
                    else:
                        seed=seed.left

    def inorder_tree-walk(x):
        pass
def create_graph(G, node, pos={}, x=0, y=0, layer=1):
    pos[node.value] = (x, y)

    if node.left:
        G.add_edge(node.value, node.left.value)
        l_x, l_y = x - 1 / 2 ** layer, y - 1
        l_layer = layer + 1
        create_graph(G, node.left, x=l_x, y=l_y, pos=pos, layer=l_layer)
    if node.right:
        G.add_edge(node.value, node.right.value)
        r_x, r_y = x + 1 / 2 ** layer, y - 1
        r_layer = layer + 1
        create_graph(G, node.right, x=r_x, y=r_y, pos=pos, layer=r_layer)
    return (G, pos)

def draw(node):   # 以某个节点为根画图
    graph = nx.DiGraph()
    graph, pos = create_graph(graph, node)
    fig, ax = plt.subplots(figsize=(8, 10))  # 比例可以根据树的深度适当调节
    nx.draw_networkx(graph, pos, ax=ax, node_size=300)
    plt.show()


if __name__ == '__main__':
    l=[40,20,30,50,13,23]
    tree=BinaryTree(l)
    tree.insert(*l)
    draw(tree.root)