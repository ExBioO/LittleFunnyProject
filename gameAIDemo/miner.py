__author__ = 'Bright'

from GameEntity import BaseGameEntity
from stateMachine import stateMachine

class miner(BaseGameEntity):
    def __init__(self, id,
                 state=None,
                 location="home",
                 goldCarried=0,
                 money=0,
                 thirst=0,
                 fatigue=0
                 ):
        self.id = id
        self.stateMachine = stateMachine(self,
                                         currentState=state if state else EnterMineAndDigForNugget
                                         )
        self.location = location
        self.goldCarried = goldCarried
        self.money = money
        self.thirst = thirst
        self.fatigue = fatigue

    def getlocation(self):
        return self.location

    def update(self):
        self.stateMachine.update()

    def receiveMessage(self, telegram):
        return self.stateMachine.handleMessage(telegram.msg)

#FSM for miner
class minerState(object):
    @classmethod
    def enter(cls, miner):
        print("Bob: enter "+cls.__name__)
    @classmethod
    def run(cls, miner):
        pass
    @classmethod
    def exit(cls, miner):
        print("Bob: exit "+cls.__name__)
    @classmethod
    def onMessage(cls, miner, msg):
        pass

class EnterMineAndDigForNugget(minerState):
    location = "mine"
    @classmethod
    def run(cls, miner):
        print("Bob: digging...")

        miner.thirst += 1
        miner.fatigue += 1
        miner.goldCarried += 1
        miner.location = cls.location

        if miner.goldCarried >= 10:
            miner.stateMachine.changeState(vistBankAndDepositGold)
        elif miner.thirst >= 10 and miner.money>0:
            miner.stateMachine.changeState(quenchThirst)
        elif miner.fatigue >= 10:
            miner.stateMachine.changeState(goHomeSleepTillRested)

class vistBankAndDepositGold(minerState):
    location = "bank"
    @classmethod
    def run(cls, miner):
        print("Bob: sell gold")

        miner.thirst += 1
        miner.money += 5*miner.goldCarried
        miner.goldCarried = 0
        miner.location = cls.location

        if miner.thirst >= 10 and miner.money > 0:
             miner.stateMachine.changeState(quenchThirst)
        elif miner.fatigue >= 10 or miner.money >= 100:
            miner.stateMachine.changeState(goHomeSleepTillRested)
        else:
            miner.stateMachine.changeState(EnterMineAndDigForNugget)

class quenchThirst(minerState):
    location = "bar"
    @classmethod
    def run(cls, miner):
        print("Bob: drinking...")

        miner.thirst -= 1 if miner.thirst>0 else 0
        miner.money -= 1
        miner.location = cls.location

        if miner.thirst > 0 and miner.money > 0:
            pass
        elif miner.fatigue >= 10 or (miner.money >= 100 and miner.fatigue > 5):
            miner.stateMachine.changeState(goHomeSleepTillRested)
        else:
            miner.stateMachine.changeState(EnterMineAndDigForNugget)

class goHomeSleepTillRested(minerState):
    location = "home"
    @classmethod
    def enter(cls, miner):
        print("Bob: enter "+cls.__name__)
        if not (miner.location == cls.location):
            miner.location = cls.location
            print("Bob: I am home" )
            miner.sendMessage(1, "I am home")
    @classmethod
    def run(cls, miner):
        print("Bob: sleeping...")

        #miner.thirst += 0.1
        miner.fatigue -= 1 if miner.fatigue>0 else 0

        if miner.fatigue > 0:
            return
        elif miner.thirst >= 10 or (miner.money >= 100 and miner.thirst>5):
            miner.stateMachine.changeState(quenchThirst)
        else:
            miner.stateMachine.changeState(EnterMineAndDigForNugget)
    @classmethod
    def onMessage(cls, miner, msg):
        if msg == "StewReady":
            miner.stateMachine.changeState(eatStew)
            return True

class eatStew(minerState):
    location = "home"
    @classmethod
    def run(cls, miner):
        print("Bob: eating Stew")
        miner.stateMachine.changeState(goHomeSleepTillRested)




