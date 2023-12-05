from common.SocketUtils import CommunicateManager
from common.MessageManager import MessageManager

class User:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.cornerIn = None

    def sendWhisperMessage(self, fromId, message):
        privateDict = MessageManager().buildWhisperDict(fromId, message)
        CommunicateManager().sendDict(privateDict, (self.ip, self.port))
        
    def sendChatMessage(self, cornerName, fromName, message):
        chatDict = MessageManager().buildChatDict(cornerName, fromName, message)
        CommunicateManager().sendDict(chatDict, (self.ip, self.port))
        
    def joinCorner(self, corner):
        self.cornerIn = corner

    def leaveCorner(self):
        self.cornerIn = None

    def getCorner(self):
        return self.cornerIn