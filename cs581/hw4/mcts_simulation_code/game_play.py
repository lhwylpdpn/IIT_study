import random

from operator import itemgetter

from game_search import minimax_decision


def maxplayer(gn, algo=minimax_decision):
    res = algo(gn)
    chosen_move_util = max(res, key = itemgetter(1))

    # util = chosen_move_util[1]
    # if util == 1:
    #     print("{} has a winning strategy".format(gn.next_player()))

    return chosen_move_util[0]



def randplayer(gb, seed=None):
    rg = random.Random(seed)
    moves = gb.available_moves()
    return rg.choice(moves)

def firstmoveplayer(gb):
    moves = gb.available_moves()
    return moves[0]

def human_player(gb, p):
    move = input("Your move, x, y separated by comma:")
    move = move.split(',')
    move[0] = int(move[0])
    move[1] = int(move[1])
    move.append(p)
    available_moves = gb.available_moves()
    if tuple(move) in available_moves:
        return tuple(move)
    else:
        print("Not a legal move.")
        print("Available moves are ", available_moves)
        print("Try again.")
        return human_player(gb, p)

def game_play(initial_node, x_player, o_player):
    current_gn = initial_node

    while not current_gn.is_terminal():
        print(current_gn)
        p = current_gn.next_player()
        print("It's {}'s turn.".format(p))

        if p == 'X':
            chosen_move = x_player(current_gn)
        else:
            chosen_move = o_player(current_gn)

        print("Chosen move {}.".format(str(chosen_move)))
        print()
        current_gn = current_gn.next_game_node(chosen_move)

    print("\nGame ended.")
    print(current_gn)

    winner = current_gn.winner()

    if winner is not None:
        print("Winner is {}.".format(winner))
    else:
        print("Draw.")

