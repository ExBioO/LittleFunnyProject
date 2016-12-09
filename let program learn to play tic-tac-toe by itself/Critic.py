from board import board
from Performance_System import AI
import numpy as np

def Critic(log, result):
    critic = AI()
    sumluator = board(3)
    data = []
    for decision in log:
        sumluator.run(decision)
        x = critic.abstract(sumluator.grid)
        if critic.order == 1:
            critic.order = 0
            item = np.array(list(x)+[100*(result==1)-100*(result==0)])
        elif critic.order == 0:
            critic.order = 1
            item = np.array(list(x)+[100*(result==0)-100*(result==1)])
        data.append(item)
    data = np.vstack(data)
    return data
    
def test():
    from Experiment_Generator import experiment
    from Performance_System import perform
    import time, os
    a = np.array([100,-100,50,50, 10, -10])
    h = lambda x: np.dot(x,a)
    exp = experiment(h)
    os.system('cls')
    print("perform start.")
    time.sleep(1)
    log, result = perform(exp, silence = False)
    print("perform finish.")
    print("data:")
    data = Critic(log, result)
    print(data, type(data))
    
if __name__ == "__main__":
    test()