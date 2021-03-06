# TODO import the necessary classes and methods
import sys
from collections import namedtuple
from games import TicTacToe
GameState = namedtuple('GameState', 'to_move, utility, board, moves')
import time 
global s_
s_=[]
global non_s_
global utility_
global non_utility_
utility_={}
non_utility_={}
non_s_=[]

def file_read(filename):
    board: Dict[Tuple[int, int], str] = {}
    i = 0
    with open(filename, 'r', encoding='utf-8') as f:
        res = f.readlines()
    for r in res:
        if len(r) > 0:
            r = r.replace('\n', '').split(' ')
            for j in range(0, len(r)):
                board[i+1, j+1] = r[j].upper()
            i += 1
    return board
def set_initial(_board):
    h,v=0,0
    res = {"X": 0, "O": 0}
    for k in _board.keys():
        h = k[0] if k[0] > h else h
        v = k[1] if k[1] > v else v
    moves = [(x, y) for x in range(1, h + 1) for y in range(1, v + 1)]
    for k in _board.keys():
        if _board[k].upper() == 'X' or _board[k].upper() == 'O':
            moves.remove(k)
    for p in _board.values():
        if p.upper() == "X":
            res['X'] += 1
        if p.upper() == "O":
            res['O'] += 1
    return GameState(to_move='O' if res["X"] > res["O"] else 'X', utility=0, board=_board, moves=moves)
class game_problem(TicTacToe):

    def __init__(self, initial_state):
        self.h=0
        self.v=0
        self.k=0
        for k in initial_state.board.keys():
            self.h=k[0] if k[0]>self.h else self.h
            self.v = k[1] if k[1] > self.v else self.v
        self.k = max(self.h,self.v)

        self.initial = initial_state
def minmax_decision_update(state, game):
    non_s_.append(state)
    player = game.to_move(state)
    print(player)
    def max_value(state):

        if game.terminal_test(state):
            s_.append(state)

            utilily=game.utility(state, player) if player.upper()=="X" else -game.utility(state, player)
            utility_[utilily]= 1 if utility_.get(utilily) is None else utility_.get(utilily)+1
            return game.utility(state, player)
        non_s_.append(state)
         
        v = -float('inf')
        for a in game.actions(state):
            v = max(v, min_value(game.result(state, a)))
        if player.upper()=='X':
            non_utility_[v]= 1 if non_utility_.get(v) is None else non_utility_.get(v)+1
        else:
            non_utility_[-v]= 1 if non_utility_.get(-v) is None else non_utility_.get(-v)+1
        return v

    def min_value(state):

        if game.terminal_test(state):
            s_.append(state)
            utilily=game.utility(state, player) if player.upper()=="X" else -game.utility(state, player)
            utility_[utilily]= 1 if utility_.get(utilily) is None else utility_.get(utilily)+1
            return game.utility(state, player)
        non_s_.append(state)
        v =  float('inf')
        for a in game.actions(state):
            v = min(v, max_value(game.result(state, a)))
        if player.upper()=='X':
            non_utility_[v]= 1 if non_utility_.get(v) is None else non_utility_.get(v)+1
        else:
            non_utility_[-v]= 1 if non_utility_.get(-v) is None else non_utility_.get(-v)+1
        return v
    res={}
    for a in game.actions(state):
        res[a]=min_value(game.result(state, a))
    v=max(res.values())
    if player.upper()=='X':
            non_utility_[v]= 1 if non_utility_.get(v) is None else non_utility_.get(v)+1
    else:
            non_utility_[-v]= 1 if non_utility_.get(-v) is None else non_utility_.get(-v)+1
    return max(res, key=res.get)


def run(state,game):
    minmax_decision_update(state, game)
    Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8='','','','','','','',''
    Q1=len(s_)
    Q2=utility_.get(1) if utility_.get(1) is not None else 0
    Q3=utility_.get(-1) if utility_.get(-1) is not None else 0
    Q4=utility_.get(0) if utility_.get(0) is not None else 0
    Q5=len(non_s_)
    print(non_utility_)
    Q6=non_utility_.get(1) if non_utility_.get(1) is not None else 0
    Q7=non_utility_.get(-1) if non_utility_.get(-1) is not None else 0
    Q8=non_utility_.get(0) if non_utility_.get(0) is not None else 0
    return Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8

if __name__ == '__main__':

    input_file = sys.argv[1]
    initial = set_initial(file_read(input_file))
    game = game_problem(initial)
    #run(initial, game)
    Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8=run(initial,game)

    # Starting from this state, populate the full game tree.
    # The leaf nodes are the terminal states.
    # The terminal state is terminal if a player wins or there are no empty squares.
    # If a player wins, the state is considered terminal, even if there are still empty squares.
    # Answer the following questions for this game tree.
    print('How many terminal states are there?')
    print(Q1)
    print('In how many of those terminal states does X win?')
    print(Q2)
    print('In how many of those terminal states does X lose?')
    print(Q3)
    print('In how many of those terminal states does X draw?')
    print(Q4)
    print('How many non-terminal states are there?')
    print(Q5)
    print('In how many of those non-terminal states does X have a guranteed win?')
    print(Q6)
    print('In how many of those non-terminal states does X have a guranteed loss?')
    print(Q7)
    print('In how many of those non-terminal states does X have a guranteed draw?')
    print(Q8)
