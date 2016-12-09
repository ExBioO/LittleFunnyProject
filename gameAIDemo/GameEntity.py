__author__ = 'Bright'

class BaseGameEntity(object):
    def __init__(self, id):
        self.id = id
    def update(self):
        pass
    def sendMessage(self, reciverid, msg, delay=0, ExtraInfo=None):
        return MessageDispatcher.dispatchMsg(self.id, reciverid, msg, delay, ExtraInfo)
    def receiveMessage(self, telegram):
        pass

#Message Deliver
from time import time as clock
from Queue import PriorityQueue

entityManager = dict()

class telegram:
    def __init__(self, senderid, receiverid, msg, dispatchTime, ExtraInfo):
        self.sender = senderid
        self.receiverid = receiverid
        self.msg = msg
        self.dispatchTime = dispatchTime
        self.ExtraInfo = ExtraInfo

class MessageDispatcher(object):
    queue = PriorityQueue()
    @classmethod
    def discharge(cls, receiver, tel):
        receiver.receiveMessage(tel)
    @classmethod
    def dispatchMsg(cls, senderid, receiverid, msg,
                 delay=0,
                 ExtraInfo=None
                 ):
        receiver = entityManager[receiverid]
        time = clock()
        tel = telegram(senderid, receiverid, msg, time+delay, ExtraInfo)
        if delay<=0:
            cls.discharge(receiver,tel)
        else:
            cls.queue.put((tel.dispatchTime, tel))
        return True
    @classmethod
    def dispatchDelayedMsg(cls):
        if cls.queue.empty(): return
        currenttime = clock()
        tel=cls.queue.get()[1]
        while(tel.dispatchTime<=currenttime):
            receiver = entityManager[tel.receiverid]
            cls.discharge(receiver, tel)
            if cls.queue.empty(): return
            tel = cls.queue.get()[1]
        cls.queue.put((tel.dispatchTime, tel))