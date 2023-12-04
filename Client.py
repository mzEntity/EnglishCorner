import logging
from common.Config import *
from client.InputParser import InputParser
from common.Cache import GlobalCache
from common.workspace.ReceiptManager import ReceiptManager
from common.SocketUtils import CommunicateManager
from common.Utils import *
    
def waitForInput():
    print(">", end="")
    message = input()
    return message


if __name__ == "__main__":
    GlobalCache().setUserInfo("id", "")
    inputParser = InputParser()
    communicateManager = CommunicateManager()
    receiptManager = ReceiptManager()

    while True:
        try:
            message = waitForInput()
            requestDict = inputParser.parseInput(message)
            communicateManager.sendDict(requestDict, server_addr)
            responseDict, addr = communicateManager.recvDict()
            receipt = receiptManager.createReceipt(responseDict)
            receipt.response()
        except Exception as e:
            logging.exception(e)
    systemEXIT()