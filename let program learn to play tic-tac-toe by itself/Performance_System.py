"""
given hypothesis and device, perform the experiment
-play tic-tac-toe with given function!
"""
import numpy as np
from agent import AI
import random

def perform(experiment, silence = True):
    a = np.array([0, 100,-100,50,-50, 10, -10])
    h = lambda x: np.dot(x,a[1:])+a[0]
    b = experiment.device
    player1 = AI(experiment.hypo)
    player2 = AI(h)
    player = [player1, player2]
    #random.shuffle(player)
    b.play(player[0], player[1], silence)
    return (b.log, b.check())

def test():
    from Experiment_Generator import experiment
    h = lambda x: np.dot(x,np.array([100,-100,50,-50, 10, -10]))
    exp = experiment(h)
    log, result = perform(exp, silence = False)
    print('log:%s\nresult:%s' % 
        (' '.join(map(lambda t: (str(t[0])+str(t[1])),log)), result)
    )
    
if __name__ == "__main__":
    test()