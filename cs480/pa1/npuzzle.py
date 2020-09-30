from search import Problem # TODO import the necessary classes and methods
from search import breadth_first_tree_search
from search import breadth_first_graph_search
from search import depth_first_graph_search
from search import depth_first_tree_search
from search import best_first_graph_search
from search import uniform_cost_search
from search import astar_search
import sys


# [BFTS, BFGS, UCTS, UCGS, GBFTS, GBFGS, ASTS, ASGS]
state_list = {}
h={}
global initial
global goal
global g
def file_read(filename):
	global initial
	global goal
	global  g
	with open(filename,'r',encoding='utf-8') as f:
		res=f.readlines()
	initial=[]
	for r in res:
		g=0
		r=r.replace('\n','')
		if r[0]=='#':
			continue
		for num in r.split(' '):
			initial.append(int(num))
			g=g+1
	initial = tuple(initial)
	goal=tuple(sorted(initial))


def return_node_from_search(search_class,problem_) -> object:

	search_class=search_class.upper()
	res_node=None
	#if search_class=='DFTS':
	#	res_node=depth_first_tree_search(problem_)
	#elif search_class=='DFGS':
	#	res_node = depth_first_graph_search(problem_)
	if search_class=='BFTS':
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
		res_node = best_first_graph_search(problem_,lambda n:sum(s != g for (s, g) in zip(n.state, goal)))
	elif search_class=='GBFGS':
		res_node = best_first_graph_search(problem_,lambda n:sum(s != g for (s, g) in zip(n.state, goal)))
	else:
		print ('Parameter 2 is incorrect. Please enter one of the following parameters [BFTS, BFGS, UCTS, UCGS, GBFTS, GBFGS, ASTS, ASGS] ')
	return res_node
class npuzzle(Problem):

	def __init__(self, initial, goal):
		super().__init__(initial,goal)

	def find_blank_square(self, state):

		return state.index(0)
	def actions(self, state):
		global g
		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)
		if index_blank_square % g == 0:
			possible_actions.remove('LEFT')
		if index_blank_square < g:
			possible_actions.remove('UP')
		if index_blank_square % g == g-1:
			possible_actions.remove('RIGHT')
		if index_blank_square > g*(g-1)-1:
			possible_actions.remove('DOWN')

		return tuple(possible_actions)
	def result(self, state, action):
		global g
		blank = self.find_blank_square(state)
		new_state = list(state)
		delta = {'UP': -g, 'DOWN': g, 'LEFT': -1, 'RIGHT': 1}
		neighbor = blank + delta[action]
		new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]
		print(new_state,self.check_solvability((new_state)))
		return tuple(new_state)

	def goal_test(self, state):

		return super().goal_test(state)
	def path_cost(self, c, state1, action, state2):
		return  c+1

	def h(self,node):

		return sum(s != g for (s, g) in zip(node.state, self.goal))

	def check_solvability(self, state):

		inversion = 0
		for i in range(len(state)):
			for j in range(i + 1, len(state)):
				if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
					inversion += 1

		return inversion % 2 == 0

if __name__ == '__main__':
	input_file = sys.argv[1]
	search_algo_str = sys.argv[2]
	# # TODO implement
	file_read(input_file)
	goal_node =return_node_from_search(str(search_algo_str),npuzzle(initial, goal)) # TODO call the appropriate search function with appropriate parameters


	# # Do not change the code below.
	#
	if goal_node is not None:
	 	print("Solution path", goal_node.solution())
	 	print("Solution cost", goal_node.path_cost)
	else:
	 	print("No solution was found.")