import logging
from common.Config import *
from common.SocketUtils import CommunicateManager
from common.workspace.CommandFactory import CommandFactory
from server.Background import Background
from common.Utils import *
import time
from server.Receiver import Receiver

def setAddrToHeader(msgDict, addr):
    msgDict["header"]["ip"] = addr[0]
    msgDict["header"]["port"] = str(addr[1])


if __name__ == "__main__":
    cmdFactory = CommandFactory()
    background = Background()
    communicateManager = CommunicateManager()
    communicateManager.bind(server_addr)
    
    # 接收数据
    while True:
        try:
            packetDict, addr = communicateManager.recvDict()

            print("received message from", addr)
            setAddrToHeader(packetDict, addr)
            cmd = cmdFactory.createCommand(packetDict)
            receiptDict = background.executeCommand(cmd)
            communicateManager.sendDict(receiptDict, addr)
            
            
        except Exception as e:
            print(e)