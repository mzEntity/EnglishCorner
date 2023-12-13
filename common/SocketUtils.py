import socket
from common.Singleton import singleton
from common.Protocol import ProtocolTranslator
from common.Config import *

@singleton
class CommunicateManager:
    def __init__(self):
        self.socketManager = SocketManager()
        self.translator = ProtocolTranslator()

    def sendDict(self, packetDict, addr):
        packetStr = self.translator.dictToStr(packetDict)
        self.socketManager.sendTo(packetStr.encode("utf-8"), addr)
        

    def recvDict(self, byteCount=1024):
        data, addr = self.socketManager.recv(byteCount)
        msg = data.decode("utf-8")
        packetDict = self.translator.strToDict(msg)
        return packetDict, addr

    def bind(self, addr):
        return self.socketManager.bind(addr)

    def close(self):
        return self.socketManager.close()
    
    def getSocket(self):
        return self.socketManager.sock
    
    def setTimeOut(self, time):
        return self.socketManager.setTimeOut(time)

@singleton
class SocketManager:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def recv(self, byteCount=1024):
        return self.sock.recvfrom(byteCount)

    def bind(self, addr):
        return self.sock.bind(addr)

    def sendTo(self, packetBytes, addr):
        return self.sock.sendto(packetBytes, addr)
    
    def setTimeOut(self, time):
        return self.sock.settimeout(time)

    def close(self):
        self.sock.close()