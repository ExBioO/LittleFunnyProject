__author__ = 'Bright'

#FSM
class stateMachine(object):
    def __init__(self, owner,
                 currentState=None,
                 previousState=None,
                 globalState=None
                 ):
        self.owner = owner
        self.currentState=currentState
        self.previousState=previousState
        self.globalState=globalState
    def changeState(self, newState):
        self.currentState.exit(self.owner)
        self.previousState = self.currentState
        self.currentState = newState
        self.currentState.enter(self.owner)
    def update(self):
        if self.globalState: self.globalState.run(self.owner)
        if self.currentState: self.currentState.run(self.owner)
    def revert(self):
        self.changeState(self.previousState)
    def handleMessage(self, msg):
        return(True if self.globalState and self.globalState.onMessage(self.owner, msg) else
            True if self.currentState and self.currentState.onMessage(self.owner, msg) else
            False
               )