import sys
from collections import namedtuple
from games import minmax_decision,alpha_beta_search,TicTacToe

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


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
def run(state_,game):
    state=state_
    while True:
        move = alpha_beta_search(state, game)
        state = game.result(state, move)
        if game.terminal_test(state):
            return game.utility(state,'X')

if __name__ == '__main__':
    input_file = sys.argv[1]
    # TODO implement
    initial = set_initial(file_read(input_file))
    game = game_problem(initial)

    print('Whose turn is it in this state?')
    print(game.to_move(initial))
    # TODO: print either X or O
    print('If both X and O play optimally from this state, does X have a guaranteed win, guaranteed loss, or guaranteed draw')
    res=run(initial,game)
    if str(res)=='-1':
        print('loss')
    if str(res)=='0':
        print('draw')
    if str(res)=='1':
        print('win')
# TODO: print one of win, loss, draw