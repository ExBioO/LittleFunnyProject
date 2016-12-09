__author__ = 'Bright'

from GameEntity import BaseGameEntity
from stateMachine import stateMachine

class minerWife(BaseGameEntity):
    def __init__(self, id,
                 state=None,
                 location = "home"
                 ):
        self.id = id
        self.stateMachine = stateMachine(self,
                                         currentState=state if state else housework,
                                         globalState=minerWifeGlobalState
                                         )
        self.location = location

    def getlocation(self):
        return self.location

    def update(self):
        self.stateMachine.update()

    def receiveMessage(self, tel):
        return self.stateMachine.handleMessage(tel.msg)

#FSM for miner
from random import random

class minerWifeState(object):
    location = "home"
    @classmethod
    def enter(cls, miner):
        pass
    @classmethod
    def run(cls, minerWife):
        pass
    @classmethod
    def exit(cls, minerWife):
        pass
    @classmethod
    def onMessage(cls, minerWife, msg):
        pass

class minerWifeGlobalState(minerWifeState):
    @classmethod
    def run(cls, minerWife):
        if random() <= 0.1:
            minerWife.stateMachine.changeState(toilet)

class toilet(minerWifeState):
    @classmethod
    def run(cls, minerWife):
        print("Elsa: in toilet")
        minerWife.stateMachine.revert()

class housework(minerWifeState):
    @classmethod
    def run(cls, minerWife):
        print("Elsa: doing housework")
    @classmethod
    def onMessage(cls, minerWife, msg):
        if msg=="I am home" or msg=="StewReady":
            print("Elsa: oh")
            minerWife.stateMachine.changeState(cookStew)
        return True

class cookStew(minerWifeState):
    StewCooked = False
    @classmethod
    def run(cls, minerWife):
        if cls.StewCooked:
            print("Elsa: Stew is ready.")
            minerWife.sendMessage(0, "StewReady")
            cls.StewCooked = not cls.StewCooked
        else:
            print("Stew is being cooked")
            minerWife.sendMessage(1, "StewReady", delay=0.001)
            cls.StewCooked = True
        minerWife.stateMachine.changeState(housework)







