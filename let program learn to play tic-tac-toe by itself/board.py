# -*- coding: utf-8 -*-
"""
Created on Sat Oct 25 16:33:36 2014

@author: Bright
"""
import numpy as np
import os
import time

class board(object):
    def __init__(self, n):
        self.size = n
        self.round = 1
        self.grid = np.array(n*[n*[' ']])
        self.log = []
    def __str__(self):
        return('_'*16+'\n'
            +'|__|_'+'_|_'.join(map(str, range(self.size)))+'_|\n'
            +'_|\n'.join([
                '|_'+str(n)+'|_'+'_|_'.join(line)
                for n, line in enumerate(self.grid)
                ])
            +'_|'
        )
    

    def run(self, decision):
        if not self.isEmpty(decision):
            raise IllegalOperation("Postion not empty")
        if self.round%2 == 1:
            self.grid[decision]='O'
        elif self.round%2 == 0:
            self.grid[decision]='X'
        else:
            raise IllegalOperation("Unkown Error")
        self.round+=1
        self.log.append(decision)
            
    def cross(self, decision):
        if self.round%2==0:
             raise IllegalOperation("Wrong Round")
        self.run(decision)
    
    def ring(self, decision):
        if self.round%2 != 1:
            raise IllegalOperation("Wrong Round")
        self.run(decision)
            

    def isEmpty(self, decision):
        if type(decision)!=tuple:
            raise TypeError("decision should be 2-tuple")
        return(self.grid[decision]==' ')
        
    def hasEmpty(self):
        return (self.grid == np.array(self.size*[self.size*[' ']])).any()
        
    def check(self):
        m = self.grid
        scope = list(m)+list(m.T)+\
            [np.array([m[i,i] for i in range(self.size)]),\
            np.array([m[i,-1-i] for i in range(self.size)])]
        oWin = any(all(line == 'O') for line in scope)
        xWin = any(all(line == 'X') for line in scope)
        if oWin:
            return 1
        elif xWin:
            return 0
        elif not self.hasEmpty(): 
            return 2
        return None

    def result(self):
        flag = self.check()
        if flag is None:
            return "On-going"
        if flag == 1:
            return "O win"
        if flag == 0:
            return "X win"
        if flag == 2:
            return "Dawrn Game"
    
    def play(self, player1, player2, silence = False):
        if not silence:
            os.system('cls')
            print('type q to quit if you are player')
            print(self)
            time.sleep(0.1)
        while(self.check() == None):
            if self.round%2==1:
                decision = player1.judge(self)
            elif self.round%2==0:
                decision = player2.judge(self)
            if decision == ('q'):
                break
            self.run(decision)
            if not silence:
                os.system('clear')
                print(self)
                time.sleep(0.1)
        if not silence:
            print('result: '+str(self.result()))

        
class expBoard(board):      
    def setState(self, round, grid):
        self.round = round
        self.grid = grid        
    def reverse(self):
        self.grid[self.log.pop(-1)] = " "
        self.round-=1
            
class IllegalOperation(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def test():
    from agent import User, AI
    AI = AI()
    User = User()
    b = board(3)
    b.play(AI, User)

if __name__ == '__main__':
    test()