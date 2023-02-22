"""
    Much of the code is inspired by https://github.com/aimacode/aima-python/
"""

import copy
import numpy as np

class GameNode:

    def __init__(self, board, parent = None) -> None:
        self.board = board

    def next_player(self) -> str:
        raise NotImplementedError

    def last_played(self) -> str:
        raise NotImplementedError

    def last_move(self) -> str:
        raise NotImplementedError

    def next_game_node(self, move):
        raise NotImplementedError

    def path(self):
        current = self
        path_back = [current]
        while current.parent is not None:
            path_back.append(current.parent)
            current = current.parent
        return reversed(path_back)

    def is_terminal(self):
        raise NotImplementedError

    def winner(self) -> str:
        raise NotImplementedError

    def available_moves(self):
        raise NotImplementedError

    def utility(self, p):
        raise NotImplementedError

class MNKNode(GameNode):

    def __init__(self, board, k = 3, parent = None, last_move = None) -> None:
        """
            state (list of lists): Each sub-list is a list of Xs, Os, and -s.
            parent (MNKNode): The parent node that was used to generate this node
        """
        super().__init__(board, parent)

        self.m = len(self.board)
        self.n = len(self.board[0])
        self.k = k

        self.lm = last_move

        self.x_c, self.o_c = self._count()

    def __repr__(self) -> str:
        res = ""
        for row in self.board:
            res += " ".join(row) + "\n"
        return res

    def _count(self):
        board_arr = np.asarray(self.board)
        x_c = np.sum(board_arr == 'X')
        o_c = np.sum(board_arr == 'O')
        return x_c, o_c

    def next_player(self) -> str:
        # X goes first
        if self.x_c == self.o_c:
            return "X"
        else:
            return "O"

    def last_played(self) -> str:
        if self.next_player() == 'X':
            return 'O'
        else:
            return 'X'

    def last_move(self):
        return self.lm

    def next_game_node(self, move):
        # move is (x, y, p)
        x, y, p = move
        assert p == self.next_player()
        assert self.board[x][y] == '-'
        assert not self.is_terminal()

        new_board = copy.deepcopy(self.board)
        new_board[x][y] = p

        return MNKNode(board=new_board, k=self.k, parent = self, last_move = copy.deepcopy(move))

    def available_moves(self):
        p = self.next_player()
        moves = []

        for i in range(self.m):
            for j in range(self.n):
                if self.board[i][j] == '-':
                    moves.append((i, j, p))

        return moves

    def _is_winner(self, p):
        return self._atleastk(p)

    def winner(self) -> str:
        if self.is_terminal():
            if self._is_winner('X'):
                return 'X'
            elif self._is_winner('O'):
                return 'O'
            else:
                return None

    def _atleastk_line(self, p, begin_x, begin_y, delta_x, delta_y):
        max_count = 0
        x = begin_x
        y = begin_y

        while (x >= 0) and (x < self.m) and (y >= 0) and (y < self.n):

            if self.board[x][y] == p:
                max_count += 1
            else:
                max_count = 0

            if max_count >= self.k:
                return True

            x += delta_x
            y += delta_y

        return False

    def _atleastk(self, p):

        one_found = False

        # cols
        for begin_y in range(0, self.n):
            one_found = self._atleastk_line(p, begin_x = self.m-1, begin_y = begin_y, delta_x = -1, delta_y = 0)
            if one_found:
                return True
        # rows
        for begin_x in range(self.m-1, -1, -1):
            one_found = self._atleastk_line(p, begin_x, begin_y = 0, delta_x = 0, delta_y = 1)
            if one_found:
                return True

        # NE diag (dx = -1, dy = +1)
        ## West edge (begin_y = 0)
        for begin_x in range(self.m-1, -1, -1):
            one_found = self._atleastk_line(p, begin_x, begin_y = 0, delta_x = -1, delta_y = 1)
            if one_found:
                return True

        ## South edge (begin_x = m-1)
        for begin_y in range(self.n):
            one_found = self._atleastk_line(p, begin_x = self.m-1, begin_y = begin_y, delta_x = -1, delta_y = 1)
            if one_found:
                return True

        # NW diag (dx = -1, dy = -1)
        ## East edge (begin_y = n-1)
        for begin_x in range(self.m-1, -1, -1):
            one_found = self._atleastk_line(p, begin_x, begin_y = self.n-1, delta_x = -1, delta_y = -1)
            if one_found:
                return True

        ## South edge (begin_x = m-1)
        for begin_y in range(self.n):
            one_found = self._atleastk_line(p, begin_x = self.m-1, begin_y = begin_y, delta_x = -1, delta_y = -1)
            if one_found:
                return True

        return False

    def _is_full(self):
        return self.x_c + self.o_c == self.m * self.n

    def is_terminal(self):
        # if no empty spot left, return true
        if self._is_full():
            return True

        # Is X a winner?
        if self._is_winner('X'):
            return True

        # Is O a winner?
        if self._is_winner('O'):
            return True

        return False

    def utility(self, p):

        o_p = 'X' if p=='O' else 'O'

        if self._is_winner(p):
            return 1 # Win is 1
        elif self._is_winner(o_p):
            return 0 # Loss is 0
        elif self._is_full():
            return 0.5 # Draw is 0.5
        else: # Non-terminal state
            return None


class ConnectFour(MNKNode):

    def __init__(self, board, parent=None, last_move=None) -> None:
        super().__init__(board, 4, parent, last_move)

    def next_game_node(self, move):
        # move is (x, y, p)
        x, y, p = move
        assert p == self.next_player()
        assert self.board[x][y] == '-'
        assert not self.is_terminal()

        new_board = copy.deepcopy(self.board)
        new_board[x][y] = p

        return ConnectFour(board=new_board, parent = self, last_move = copy.deepcopy(move))

    def available_moves(self):
        p = self.next_player()
        moves = []

        # In  each column, the most bottom (highest x value) empty square
        for y in range(self.n):
            for x in range(self.m-1, -1, -1):
                if self.board[x][y] == '-':
                    moves.append((x, y, p))
                    break

        return moves

class DictGameNode(GameNode):

    _moves = None # A dictionary of moves (list) available at each state; a move is also the name of the next state
    _terminal_nodes = None # Key value pairs for the terminal states

    def __init__(self, board, np, parent = None, last_move = None) -> None:
        """
            state (list of lists): Each sub-list is a list of Xs, Os, and -s.
            parent (MNKNode): The parent node that was used to generate this node
        """
        super().__init__(board, parent)

        self.np = np
        self.lm = last_move

    def __repr__(self) -> str:
        return str(self.board)

    def next_player(self) -> str:
        return self.np

    def last_played(self) -> str:
        if self.next_player() == 'X':
            return 'O'
        else:
            return 'X'

    def last_move(self):
        return self.lm

    def next_game_node(self, move):
        # move is the name of the next board
        _np = None
        if self.np == 'X':
            _np = 'O'
        else:
            _np = 'X'

        return DictGameNode(board=move, parent = self, np = _np, last_move = move)

    def available_moves(self):
        if self.is_terminal():
            return []
        else:
            return DictGameNode._moves[self.board]

    def winner(self) -> str:

        if self.is_terminal():
            util = DictGameNode._terminal_nodes[self.board]
            if util == 1:
                return 'X'
            elif util == -1:
                return 'O'
            else:
                return None
        else:
            return None


    def is_terminal(self):
        return self.board in DictGameNode._terminal_nodes

    def utility(self, p):
        if self.is_terminal():
            if p == 'X':
                return DictGameNode._terminal_nodes[self.board]
            else:
                return -1*DictGameNode._terminal_nodes[self.board]
        else:
            return None