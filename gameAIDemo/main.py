__author__ = 'Bright'

#main loop
from time import sleep
from miner import miner
from minerWife import minerWife
from GameEntity import entityManager, MessageDispatcher

def main():
    Bob = miner(0)
    Elsa = minerWife(1)
    entityManager.update({0:Bob, 1:Elsa})
    cond=True
    count = 0
    while(cond):
        for i in range(10):
            MessageDispatcher.dispatchDelayedMsg()
            Bob.update()
            Elsa.update()
            #i=raw_input()
            count+=1

        print("count:%d\n\tthirst:%d\n\tfatigue:%d\n\tmoney:%d\n" % (count, Bob.thirst, Bob.fatigue, Bob.money))
        if Bob.thirst>30 or Bob.fatigue>30:
            print("Bob dead")
            cond = False
        elif Bob.money > 200:
            print("Bob become rich")
            cond = False
        elif Bob.money < -100:
            print("Bob bankrupted")
            cond = False

main()
