import numpy as np
import matplotlib.pylab as plt
import time

from Critic import Critic
from Experiment_Generator import experiment
from Generalizer import generalizer1, generalizer2
from Performance_System import perform

def plotTrainingProcess(winner_list, gap):
    times = [gap*i for i in range(len(winner_list)/gap)]
    winning_ratio = [sum(winner_list[i:i+gap])/gap for i in times]
    plt.figure()
    plt.plot(times, winning_ratio)
    plt.xlabel('Times')
    plt.ylabel('Winning_ratio')
    plt.title('Training Process')
    plt.show()

def training(init_a, generalizer, times = 10, silence = True):
    a = init_a
    winner_list = []
    for i in range(times):
        h = lambda x: np.dot(x, a[1:])+a[0]
        exp = experiment(h)
        log, result = perform(exp, silence = silence)
        if result == 2:
            winner_list.append(0.5)
            continue
        winner_list.append(result)
        data = Critic(log, result)
        a = generalizer(a, data)
        if not silence:
            print('log:%s\nresult:%s' % 
                (' '.join(map(lambda t: (str(t[0])+str(t[1])),log)), result)
            )
            print("data:")
            print(data)
            print("new a:", a)
            time.sleep(3)
    return a, winner_list

def main():
    init_a = np.array([0,0,0,0,0,0,0])
    a, winner_list = training(init_a, generalizer1, times = 10, silence = False)
    print("final hypo:", a)
    plotTrainingProcess(winner_list, 4)

if __name__ == '__main__':
    main()
