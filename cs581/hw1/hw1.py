import os


#best first search
#记录所有节点之间的信息和cost
from search import Problem # TODO import the necessary classes and methods
from search import breadth_first_tree_search
from search import breadth_first_graph_search
from search import depth_first_graph_search
from search import depth_first_tree_search
from search import best_first_graph_search
from search import uniform_cost_search
from search import astar_search
state_list = {}


class hw1:
    def __init__(self):
        self.graph = {}
        self.cost = {}
        self.frontier = []

        self.path = []
        self.goal = "G"
        self.start = 'S'
        self.goal_path = []
        self.goal_cost = 0
        self.heuristic = {}
    def data_init(self,start_node,end_node,cost):
        self.graph[str(start_node)+'_'+str(end_node)] = cost
        self.graph[str(end_node)+'_'+str(start_node)] = cost
    def test(self):
        print(self.graph)
        print(self.heuristic)
        return self.graph,self.heuristic
    #启发式函数
    def heuristic_init(self,node,cost):
        self.heuristic[node] = cost
    def clac_g(self,start_node,end_node):
        return self.graph[str(start_node)+'_'+str(end_node)]
    def explored(self,node):

        explored_list = {}
        for k in self.graph.keys():
            if k.split('_')[0] == node:
                explored_list[k.split('_')[1]] = self.graph[k]
        return explored_list
    def explored_by_h(self,node):
        explored_list = {}
        for k in self.graph.keys():
            if k.split('_')[0] == node:
                explored_list[k.split('_')[1]] = self.heuristic[k.split('_')[1]]
        return explored_list

    def consistent(self):
        #每一个h(n)都小于等于从n到目标的实际代价
        for k in self.graph.keys():
            if self.heuristic[k.split('_')[0]] - self.heuristic[k.split('_')[1]] > self.graph[k]:
                print('h(n) is not consistent','h1',k.split('_')[0],self.heuristic[k.split('_')[0]],k.split('_')[1],self.heuristic[k.split('_')[1]],k,self.graph[k])
                return False
        return True
    def get_consistent(self,goal):
        #获取每个节点最低cost
        nodes=[]
        for k in  self.graph.keys():
            nodes.append(k.split('_')[0])
        #nodes去重
        nodes=list(set(nodes))

    def recursion_g(self,node_start,goal,g):
        if node_start!=goal:
            tmp_dict={}
            for n in list(hw.explored(node_start).keys()):
                tmp_dict[node_start+"_"+n]=self.graph[node_start+"_"+n]
            print(tmp_dict)
            f=zip(tmp_dict.values(),tmp_dict.keys())
            c=sorted(f)
            print(c)
            min_k=c[0][1]
            min_v=c[0][0]

            print(min_k, min_v, g)
            g+=min_v
            self.graph.pop(min_k)
            self.graph.pop(min_k.split('_')[1]+'_'+min_k.split('_')[0])

            self.recursion_g(min_k.split('_')[1], goal, g)

        else:
            print('jieguo',g)


class travel(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)

    def actions(self, state):
        state_allow_actions = {}
        for k in state_list.keys():
            stateA = k.split('_')[0]
            stateB = k.split('_')[1]

            state_allow_actions[stateA] = stateB if not state_allow_actions.get(
                    stateA) else state_allow_actions.get(stateA) + stateB
            state_allow_actions[stateB] = stateA if not state_allow_actions.get(
                    stateB) else state_allow_actions.get(stateB) + stateA
        return tuple(state_allow_actions.get(state))

    def result(self, state, action):

        return action

    def goal_test(self, state):

        return super().goal_test(state)

    def path_cost(self, c, state1, action, state2):
        state_path_cost = {}
        for k in state_list.keys():
            stateA = k.split('_')[0]
            stateB = k.split('_')[1]

            state_path_cost[stateA + "_" + stateB] = int(state_list[k])
            state_path_cost[stateB + "_" + stateA] = int(state_list[k])
        return c + state_path_cost.get(str(state1) + "_" + str(state2))

    def h(self, node):

        return h.get(node.state)


def return_node_from_search(search_class,problem_) -> object:

	search_class=search_class.upper()
	res_node=None
	if search_class=='DFTS':
		res_node=depth_first_tree_search(problem_)
	elif search_class=='DFGS':
		res_node = depth_first_graph_search(problem_)
	elif search_class=='BFTS':
		res_node = breadth_first_tree_search(problem_)
	elif search_class=='BFGS':
		res_node = breadth_first_graph_search(problem_)
	elif search_class=='UCTS':
		res_node = uniform_cost_search(problem_)
	elif search_class=='UCGS':
		res_node = uniform_cost_search(problem_)
	elif search_class=='ASTS':
		res_node = astar_search(problem_)
	elif search_class=='ASGS':
		res_node = astar_search(problem_)
	elif search_class=='GBFTS':
		res_node = best_first_graph_search(problem_,lambda n:h[n.state])
	elif search_class=='GBFGS':
		res_node = best_first_graph_search(problem_,lambda n:h[n.state])
	else:
		print ('Parameter 2 is incorrect. Please enter one of the following parameters [DFTS, DFGS, BFTS, BFGS, UCTS, UCGS, GBFTS, GBFGS, ASTS, ASGS] ')
	return res_node
if __name__ == '__main__':
    hw=hw1()
    hw.data_init('A','B',4)
    hw.data_init('A','S',4)
    hw.data_init('A','F',5)
    hw.data_init('B','C',4)
    hw.data_init('B','D',3)
    hw.data_init('D','E',4)
    hw.data_init('D','G',5)
    hw.data_init('E','F',3)
    hw.data_init('E','G',2)
    hw.data_init('F','H',1)
    hw.data_init('G','H',5)
    hw.data_init('I','J',4)
    hw.data_init('I','M',6)
    hw.data_init('I','N',7)
    hw.data_init('I','S',6)
    hw.data_init('J','K',3)
    hw.data_init('J','L',3)
    hw.data_init('J','S',5)
    hw.data_init('K','L',3)
    hw.data_init('L','W',7)
    hw.data_init('L','X',8)
    hw.data_init('L','Y',9)
    hw.data_init('M','N',8)
    hw.data_init('M','R',5)
    hw.data_init('M','T',3)
    hw.data_init('M','U',4)
    hw.data_init('N','O',2)
    hw.data_init('N','P',3)
    hw.data_init('N','Q',4)
    hw.heuristic_init('A',8)
    hw.heuristic_init('B',4)
    hw.heuristic_init('C',8)
    hw.heuristic_init('D',2)
    hw.heuristic_init('E',2)
    hw.heuristic_init('F',5)
    hw.heuristic_init('G',0)
    hw.heuristic_init('H',5)
    hw.heuristic_init('I',7)
    hw.heuristic_init('J',8)
    hw.heuristic_init('K',11)
    hw.heuristic_init('L',11)
    hw.heuristic_init('M',13)
    hw.heuristic_init('N',14)
    hw.heuristic_init('O',15)
    hw.heuristic_init('P',17)
    hw.heuristic_init('Q',18)
    hw.heuristic_init('R',18)
    hw.heuristic_init('S',10)
    hw.heuristic_init('T',16)
    hw.heuristic_init('U',18)
    hw.heuristic_init('W',18)
    hw.heuristic_init('X',20)
    hw.heuristic_init('Y',20)
    state_list,h = hw.test()

    #print(state_list)
    initial = 'S'
    goal = 'G'
    goal_node = return_node_from_search("UCTS", travel(initial, goal))
    #g,h=hw.test()

    for key in h.keys():
         print('h('+key+') = '+ str(return_node_from_search("UCTS", travel(key, goal)).path_cost))
         hw.heuristic_init(node=key,cost=return_node_from_search("UCTS", travel(key, goal)).path_cost)
    now = 'E'
    print('g', hw.explored(now))
    print('h', hw.explored_by_h(now))
    goal_node = return_node_from_search("UCTS", travel(initial, goal))
    print(goal_node.solution())
    print(goal_node.path_cost)