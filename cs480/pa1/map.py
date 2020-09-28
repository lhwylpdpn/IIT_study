from search import Problem # TODO import the necessary classes and methods
from search import breadth_first_tree_search
import sys

# state is  S A B C ...etc
# action is   if A only to C  ,or to B
# result is  S + acion =A
# path_cost A + action --C  is  2
# S A > 2
# S C <> 6
# C E <> 4
# C D > 3
# A D > 3
# D E <> 4
# A B <> 5
# B G <> 7
# E G <> 3
from typing import List, Any

result_list = {}
action_list = {}
action_list['S_A'] = ">"
action_list['S_C'] = "<>"
action_list['C_E'] = "<>"
action_list['C_D'] = ">"
action_list['A_D'] = ">"
action_list['D_E'] = "<>"
action_list['A_B'] = "<>"
action_list['B_G'] = "<>"
action_list['E_G'] = "<>"

result_list['S_A'] = 2
result_list['S_C'] = 6
result_list['C_E'] = 4
result_list['C_D'] = 3
result_list['A_D'] = 3
result_list['D_E'] = 4
result_list['A_B'] = 5
result_list['B_G'] = 7
result_list['E_G'] = 3


class travel(Problem):
	def __init__(self, initial, goal):
		super().__init__(initial,goal)
	def actions(self, state):  # whatever > or <> , actually only one action as  run from stateA  - stateB
		possible_actions = '>'
		return possible_actions

	def result(self, state, action='>'):
		state_allow_result = {}
		for k in action_list.keys():
			stateA = k.split('_')[0]
			stateB = k.split('_')[1]
			if action_list[k] == ">":

				state_allow_result[stateA] = stateB if not state_allow_result.get(stateA) else state_allow_result.get(stateA) + "," + stateB
			elif action_list[k] == "<>":

				state_allow_result[stateA] = stateB if not state_allow_result.get(stateA) else state_allow_result.get(
					stateA) + "," + stateB
				state_allow_result[stateB] = stateA if not state_allow_result.get(stateB) else state_allow_result.get(
					stateB) + "," + stateA

		return tuple(state_allow_result.get(state).split(','))
	def goal_test(self, state):

		return super().goal_test(state)
	def path_cost(self, c, state1, action, state2):
		return c + 1

	def h(self, node):
		return 3


if __name__ == '__main__':
	# input_file = sys.argv[1]
	# search_algo_str = sys.argv[2]

	# TODO implement

	# goal_node = # TODO call the appropriate search function with appropriate parameters

	# Do not change the code below.

	# if goal_node is not None:
	# 	print("Solution path", goal_node.solution())
	# 	print("Solution cost", goal_node.path_cost)
	# else:
	# 	print("No solution was found.")

	test = travel('S', 'G')
	#print(test.result('A',2))
	#print(test.goal_test('S'))