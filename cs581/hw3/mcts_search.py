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
        #实现蒙特卡洛搜索树的选择过程
        #如果当前节点是叶子节点，返回当前节点
        #如果当前节点不是叶子节点，选择当前节点的最大U/N值的子节点，递归调用select_leaf
        #print('传入的mcnode',mcnode)
        if mcnode.gn.is_terminal():
            # this node is terminal
            return mcnode
        if mcnode.children is None:
            return mcnode

        max_child = mcnode.children[0]
        #print('max_child start is ',max_child)
        for child in mcnode.children:
            if util_f(child) > util_f(max_child):
                max_child = child
        #print('max_child is ',max_child)
        return select_leaf(max_child, util_f)

    def expand(mcnode, rg):
        '''Given a leaf node, if its a terminal node, return it.
        Otherwise, create all of its children and return one at random.'''
        #实现蒙特卡洛搜索树的扩展过程
        #如果当前节点是终止节点，返回当前节点
        #如果当前节点不是终止节点，创建当前节点的所有子节点，随机返回一个子节点
        if mcnode.gn.is_terminal():
            #print('terminal')
            return mcnode
        else:
            #print('not terminal')
            children = []
            for move in mcnode.gn.available_moves():
                children.append(MCNode(mcnode.gn.next_game_node(move), parent = mcnode))
            #print(children)
            mcnode.children = children
            #print('mcnode.children',mcnode.children)
            res=rg.choice(children)
            #print('choose is ',res)
            return res

    def simulate(mcnode, rg):
        '''Starting from mcnode, choose moves at random until the terminal node.
        Return the utility of the terminal node from the perspective of X.'''
        #实现蒙特卡洛搜索树的模拟过程
        #从当前节点开始，随机选择下一步，直到终止节点
        #返回终止节点对X的实用值
        #获得当前node的player
        #print('mcnode',mcnode)

        player=mcnode.gn.last_played()
        #print('player',player)
        while not mcnode.gn.is_terminal():

            move=rg.choice(mcnode.gn.available_moves())
            mcnode=MCNode(mcnode.gn.next_game_node(move), parent = mcnode)
        #print('simulatelastmcnode',mcnode,mcnode.gn.utility(player))
        res=mcnode.gn.utility(player)


        return res
    def backprop(mcnode, util):
        '''Backprob the simulation to the ancestor nodes.
        Increment N for all ancestor nodes. Update the util for the correct side.'''
        #实现蒙特卡洛搜索树的反向传播过程
        #从当前节点开始，向上更新祖先节点的N和U
        u_tmp=util
        while mcnode is not None:


            mcnode.N += 1
            mcnode.U += u_tmp
            #获取当前节点的player
            player=mcnode.gn.next_player()
            #print('playerback',player)
            #print('backpropmcnode',mcnode,mcnode.U,mcnode.N)
            mcnode = mcnode.parent
            u_tmp=1-u_tmp
    
    # Body of the search
    root_mcnode = MCNode(root_gn)
    rg = random.Random(seed)

    for _ in range(max_iter):
        leaf_mcnode = select_leaf(root_mcnode, util_func)
        #print('首选选择了',leaf_mcnode)
        child_mcnode = expand(leaf_mcnode, rg)
        #print('扩展选了子节点',child_mcnode)
        util = simulate(child_mcnode, rg)
        #print('选择节点的最终分',util)
        backprop(child_mcnode, util)
        #print('反向传播完毕')
    return root_mcnode


