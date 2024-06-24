import copy
import random

#Constants
P_ONE = "X"
P_TWO = "O"

class Grid:
    def __init__(self, dim = 3):
        self._grid = [[None for dummycol in range(dim)] for dummyrow in range(dim)]
        self._dim = dim
        self._current_player = P_ONE
    
    def __str__(self):
        g = [[self._grid[row][col] if self._grid[row][col] != None else " " for col in range(self._dim)] for row in range(self._dim)]
        s = "Grid: \n"
        for c in g[:-1]: 
            s += "|".join(c)
            s += "\n"
            s += "- "*self._dim
            s += "\n"
        s += "|".join(g[-1])
        return s + "\n"
    
    def get_dim(self):
        return self._dim
    
    def get_grid(self):
        return self._grid
    
    def find_moves(self):
        moves = []
        for col in range(self._dim):
            for row in range(self._dim):
                if not self._grid[row][col] :
                    moves.append((row, col))
        return moves

    def make_move(self, move, player):
        if player != self._current_player:
            print("Not Player's Move")
            return
        row, col = move[0], move[1]
        if not self._grid[row][col]:
            self._grid[row][col] = player
            
        self.switch_player(player)

    def get_current_player(self):
        return self._current_player
    
    def switch_player(self, player):
        if player == P_ONE:
            self._current_player  = P_TWO
        else:
            self._current_player = P_ONE

    def check_win(self): 
        winone = [P_ONE]*self._dim
        wintwo = [P_TWO]*self._dim
            
        for row in range(self._dim):
            if self._grid[row] == winone:
                return P_ONE
            elif self._grid[row] == wintwo:
                return P_TWO
        
        for col in range(self._dim):
            column = [self._grid[row][col] for row in range(self._dim)]
            if column == winone:
                return P_ONE
            if column == wintwo:
                return P_TWO
            
        diaone = [self._grid[i][i] for i in range(self._dim)]
        if diaone == winone:
            return P_ONE
        if diaone == wintwo:
            return P_TWO
        
        diatwo = [self._grid[i][self._dim - 1 - i] for i in range(self._dim)]   
        if diatwo == winone:
            return P_ONE
        elif diatwo == wintwo:
            return P_TWO

        return False
        
    def check_game_over(self):
        if self.check_win() or len(self.find_moves())==0:
            return True
        return False
    
    def get_score(self, player):
        if not self.check_game_over():
            return False
        winner = self.check_win()
        if winner == player:
            return 1
        elif not winner:
            return 0
        else:
            return -1
    
class GameNode:
    def __init__(self, board):
        self._value = board
        self._children = []
        self._score = 0
        #self._moves = []
        self._best_moves = []

    def __str__(self):
        s = "\n"
        s += str(self._value)
        for child in self._children:
            s += "\n"
            s += str(child)
        return s 
    
    def get_value(self):
        return self._value
    
    def get_children(self):
        for child in self._children:
            yield child

    def print_children(self):
        ids = [id(c) for c in self._children]
        print(ids)

    def count_children(self):
        return len(self._children)
    
    def get_score(self):
        return self._score
    
    def get_moves(self):
        return self._best_moves
    
    def add_child(self, child):
        self._children.append(child)
    
    def add_score(self, score):
        self._score = score

    def add_move(self, move):
        self._best_moves.append(move)
            

def compute_next_move(node, player):
    board = node.get_value()
    if board.check_game_over():
        score = board.get_score(player)
        node.add_score(score)
        return
    
    moves = board.find_moves()

    for move in moves:
        new_board = copy.deepcopy(board)
        new_board.make_move(move, board.get_current_player())
        child = GameNode(new_board)
        node.add_child(child)
        compute_next_move(child, player)
    
    scores = [(child.get_score(), moves[i]) for i, child in enumerate(node.get_children())]
    if board.get_current_player() == player:
        final_scores = list(filter(lambda x: x[0]==max(scores)[0], scores))
    else:
        final_scores= list(filter(lambda x: x[0]==min(scores)[0], scores))
    for score, move in final_scores:
        node.add_move(move)
        node.add_score(score)

    return node.get_moves()

x = Grid(dim=3)
x._grid = [["O",None,None],
           [None,"X",None],
           [None,None,"O"]]
game = GameNode(x)
print(compute_next_move(game, P_ONE))


