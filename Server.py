import logging
from common.Config import *
from common.SocketUtils import CommunicateManager
from common.workspace.CommandFactory import CommandFactory
from server.Background import Background
from common.Utils import *
import time
from server.Receiver import Receiver
from common.ConsoleManager import ConsoleManager

def setAddrToHeader(msgDict, addr):
    msgDict["header"]["ip"] = addr[0]
    msgDict["header"]["port"] = str(addr[1])


if __name__ == "__main__":
    cmdFactory = CommandFactory()
    background = Background()
    communicateManager = CommunicateManager()
    communicateManager.bind(server_addr)
    communicateManager.setTimeOut(3)
    timer = time.time()
    # 接收数据
    while True:
        try:
            try:
                packetDict, addr = communicateManager.recvDict()
                ConsoleManager().print(f"received message from {addr}")
                setAddrToHeader(packetDict, addr)
                cmd = cmdFactory.createCommand(packetDict)
                receiptDict = background.executeCommand(cmd)
                communicateManager.sendDict(receiptDict, addr)
            except TimeoutError as e:
                pass
            if time.time() - timer > 600:
                Receiver().checkTime()
                timer = time.time()
        except Exception as e:
            # ConsoleManager().print(e)
            logging.exception(e)