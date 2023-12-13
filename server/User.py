from common.SocketUtils import CommunicateManager
from common.MessageManager import MessageManager
import time
from common.Config import *

class User:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.cornerIn = None
        self.sessionStartTime = time.time()

    def sendWhisperMessage(self, fromId, message):
        privateDict = MessageManager().buildWhisperDict(fromId, message)
        CommunicateManager().sendDict(privateDict, (self.ip, self.port))
        
    def sendChatMessage(self, cornerName, fromName, message):
        chatDict = MessageManager().buildChatDict(cornerName, fromName, message)
        CommunicateManager().sendDict(chatDict, (self.ip, self.port))
        
    def sendSystemMessage(self, message):
        systemDict = MessageManager().buildSystemDict(message)
        CommunicateManager().sendDict(systemDict, (self.ip, self.port))
        
    def joinCorner(self, corner):
        self.cornerIn = corner

    def leaveCorner(self):
        self.cornerIn = None

    def getCorner(self):
        return self.cornerIn
    
    def outOfDate(self):
        now = time.time()
        return now - self.sessionStartTime > session_time
    
    def sendOutOfDateMessage(self):
        systemDict = MessageManager().buildOutOfDateDict()
        CommunicateManager().sendDict(systemDict, (self.ip, self.port))