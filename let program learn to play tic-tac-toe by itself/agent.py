import itertools
import numpy as np
import random
from board import expBoard

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    ans, maxval = [], None
    key = key or (lambda x: x)
    for i in iterable:
        if not ans or key(i) > maxval: 
            ans, maxval = [i], key(i)
        elif key(i) == maxval:
            ans.append(i)
    return ans

class AI():
    """build a experimental game player with given hypothesis"""
    def __init__(self, core = None, order = 1):
        self.core = core or (lambda x:
            np.dot(x,np.array([100,-10, 20,-100, 10, -10]))
        )
        self.expBoard = expBoard(3)
        self.order = order
    def __str__(self):
        return 'AI'

    def judge(self, board):
        b = self.expBoard
        b.setState(board.round, board.grid)
        self.order = b.round%2
        decisionlist = filter(b.isEmpty, 
            itertools.product(range(b.size), range(b.size)))                
        bestDecisionlist = allmax(decisionlist, key = self.score)
        return random.choice(bestDecisionlist)
        
    def score(self, decision):
        """score the decision by run the decision and validate the 
        followed grid using core function.
        """
        b = self.expBoard
        b.run(decision)
        x = self.abstract(b.grid)
        try:
            score = self.core(x)
        except ValueError:
            print("ValueError x:",x)
        b.reverse()
        return score
        
    def abstract(self, grid):
        """
        abstract following feature from grid:
        x1 = the number of 3-line in our side;
        x2 = the number of 3-line in oppsite side;
        x3 = line with one empty and our marks;
        x4 = line with one empty and oppsite's marks;
        x5 = line with two empty and our mark;
        x6 = line with two empty and oppsite's mark;
        """
        size = grid.shape[0]
        scope = list(grid)+list(grid.T)+\
            [np.array([grid[i,i] for i in range(size)]),\
            np.array([grid[i,-1-i] for i in range(size)])]
        if self.order==0: R = "X"; B = "O"
        if self.order==1: R = "O"; B = "X"
        x1 = len(filter(lambda line: all(line==R), scope))
        x2 = len(filter(lambda line: all(line==B), scope))
        x3 = len(filter(lambda line: all(np.sort(line)==[" ", R, R]), scope))
        x4 = len(filter(lambda line: all(np.sort(line)==[" ", B, B]), scope))
        x5 = len(filter(lambda line: all(np.sort(line)==[" ", " ", R]), scope))
        x6 = len(filter(lambda line: all(np.sort(line)==[" ", " ", B]), scope))
        x = np.array([x1,x2,x3,x4,x5,x6])
        return x

class User():
    def __init__(self):
        pass
    def __str__(self):
        return 'User'
    def judge(self, board):
        while(True):
            decision = raw_input('round '+str(board.round)+'> ').split(' ')
            decision = tuple(decision)
            try:
                if decision == ('q') or (len(decision) == 2 and board.isEmpty(decision)):
                    break
            except:
                print("invalid input")
        return decision
        