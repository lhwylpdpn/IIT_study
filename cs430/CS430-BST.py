#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    
    def __init__(self, value, left=None, right=None,p=None):
        self.value = value   # 节点的值
        self.left = left     # 左子节点
        self.right = right   # 右子节点
class BinaryTree:

    def __init__(self, root=None):
       
        self.root =root


    def tree_minimum(self,nodex):#寻找后继
        x=nodex

        while x.left:
            x=x.left

        return x

    def insert(self,z):
        y=None
        x=self.root
        
        while x!=None:
    
            y=x
            if z.value<x.value:
                x=x.left
            else:
                x=x.right

        if y==None:
            self.root=z
        elif z.value<y.value:
            y.left=z
        else:
            y.right=z

    def delete(self,z):
        #1 |  z 没有child 直接删
        #2 |  Z 有1个left 直接，left 替换Z
        #3 |  Z 有1个right ，right节点代替Z

        #4 |  Z 既有left 也有 right 找后继在哪边儿， 后继在right， 直接将right子树替换z的位置 ，后继在left，用left的right替换left本身，再用left 替换z
        #if z.left==None and z.right==None:
        z=self.find_node(z)
        if z==None:
        	return self.root
        if z.left==None:
            self.transplant(z,z.right)
        elif z.right==None:
            self.transplant(z,z.left)
        else:
            
            y=self.tree_minimum(z.right)
           
            y_p=self.find_parent_node(y)
            print(y_p.value)
            if y_p!=z:
                self.transplant(y,y.right)
                y.right=z.right
            self.transplant(z,y)
            y.left=z.left
        return self.root
    def find_parent_node(self,x):#寻找父节点
        node_x=self.root
        parent_=None
        while node_x and x.value!=node_x.value:
            if x.value<node_x.value:
                parent_=node_x
                node_x=node_x.left
            else:
                parent_=node_x
                node_x=node_x.right
        return parent_

    def find_node(self,x):#寻找节点
  		
        node_x=self.root
        while node_x and x.value!=node_x.value:
            if x.value<node_x.value:
                node_x=node_x.left
            else:
                node_x=node_x.right
        return node_x

    def transplant(self,u,v):#将v节点替换成u节点
        u_p=self.find_parent_node(u)
        if u_p==None:
            self.root=v
        elif u==u_p.left:
            u_p.left=v
        else:
            u_p.right=v        

    def printtree(self):
    	node_x=self.root
    	while nodex:


def create_graph(G, node, pos={}, x=0, y=0, layer=1):
    pos[node.value] = (x, y)
    #print('a',node.value,x,y)
    if node.left:
        G.add_edge(node.value, node.left.value)
        l_x, l_y = x - 1 / 2 ** layer, y - 1
        l_layer = layer + 1
       #print('left',G,node.left,l_x,l_y,pos,l_layer)
        create_graph(G, node.left, x=l_x, y=l_y, pos=pos, layer=l_layer)
    if node.right:
        G.add_edge(node.value, node.right.value)
        r_x, r_y = x + 1 / 2 ** layer, y - 1
        r_layer = layer + 1
        #print('right',G,node.right,r_x,r_y,pos,r_layer)
        create_graph(G, node.right, x=r_x, y=r_y, pos=pos, layer=r_layer)
    return (G, pos)

def draw(node):   # 以某个节点为根画图
    graph = nx.DiGraph()
    graph, pos = create_graph(graph, node)
    
    fig, ax = plt.subplots(figsize=(8, 10))  # 比例可以根据树的深度适当调节
    nx.draw_networkx(graph, pos, ax=ax, node_size=300)
    plt.show()


if __name__ == '__main__':

	#外界输入永远是新Node对象，Node.value是值

    list_=[10,2,13,11,20,12,14,15]
    tree=BinaryTree()

    for x in list_:
        tree.insert(Node(x))
     
    #x=tree.find_parent_node(Node(10))
    draw(tree.root)
    tree.delete(Node(14))
    draw(tree.root)