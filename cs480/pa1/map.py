from search import Problem # TODO import the necessary classes and methods
from search import breadth_first_tree_search
from search import breadth_first_graph_search
from search import depth_first_graph_search
from search import depth_first_tree_search
from search import uniform_cost_search
from search import astar_search
import sys
# [DFTS, DFGS, BFTS, BFGS, UCTS, UCGS, GBFTS, GBFGS, ASTS, ASGS]
state_list = {}
h={}
global initial
global goal
def file_read(filename):
	global initial
	global goal
	with open(filename,'r',encoding='utf-8') as f:
		res=f.readlines()
	tag=0
	for r in res:
		if 'Edges and their costs' in r:
			tag=1
		if 'The start and the goal state' in r:
			tag=2
		if 'Heuristic function' in r:
			tag=3
		if r[0]=='#':
			continue
		if tag==1:
			tmp=r.replace('\n','').split(' ')
			state_list[tmp[0]+"_"+tmp[1]]=[tmp[2],int(tmp[3])]
		if tag==2:
			tmp = r.replace('\n', '').split(' ')
			initial=tmp[0]
			goal=tmp[1]
		if tag==3:
			tmp = r.replace('\n', '').split(' ')
			h[tmp[0]]=int(tmp[1])

class travel(Problem):
	def __init__(self, initial, goal):
		super().__init__(initial,goal)
	def actions(self, state):
		state_allow_actions={}
		for k in state_list.keys():
			stateA = k.split('_')[0]
			stateB = k.split('_')[1]
			if state_list[k][0]== ">":
				state_allow_actions[stateA]=stateB if not state_allow_actions.get(stateA) else state_allow_actions.get(stateA)+stateB
			elif state_list[k][0]== "<>":
				state_allow_actions[stateA]=stateB if not state_allow_actions.get(stateA) else state_allow_actions.get(stateA)+stateB
				state_allow_actions[stateB]=stateA if not state_allow_actions.get(stateB) else state_allow_actions.get(stateB)+stateA
		return tuple(state_allow_actions.get(state))
	def result(self, state, action):

		return action
	def goal_test(self, state):

		return super().goal_test(state)
	def path_cost(self, c, state1, action, state2):
		state_path_cost={}
		for k in state_list.keys():
			stateA = k.split('_')[0]
			stateB = k.split('_')[1]
			if state_list[k][0] == ">":
				state_path_cost[stateA+"_"+stateB] = state_list[k][1]
			elif state_list[k][0] == "<>":
				state_path_cost[stateA + "_" + stateB] = state_list[k][1]
				state_path_cost[stateB + "_" + stateA] = state_list[k][1]
		return c+state_path_cost.get(str(state1)+"_"+str(state2))

	def h(self,node):

		return h.get(node.state)


if __name__ == '__main__':
	input_file = sys.argv[1]
	# search_algo_str = sys.argv[2]
	# TODO implement
	file_read(input_file)
	# goal_node = # TODO call the appropriate search function with appropriate parameters

	# Do not change the code below.

	# if goal_node is not None:
	# 	print("Solution path", goal_node.solution())
	# 	print("Solution cost", goal_node.path_cost)
	# else:S
	# 	print("No solution was found.")

	p = travel(initial, goal)
	res=astar_search(p)
	#res=depth_first_tree_search(p)
	print(res.solution())
	print(res.path_cost)



