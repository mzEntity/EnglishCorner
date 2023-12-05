import logging
from common.Config import *
from client.InputParser import InputParser
from common.Cache import GlobalCache
from common.workspace.ReceiptManager import ReceiptManager
from common.SocketUtils import CommunicateManager
from common.Utils import *
import select
    

if __name__ == "__main__":
    GlobalCache().setUserInfo("id", "")
    inputParser = InputParser()
    communicateManager = CommunicateManager()
    receiptManager = ReceiptManager()
    
    print("> ", end="")
    sys.stdout.flush()
    
    sock = communicateManager.getSocket()
    inputs = [sys.stdin, sock]
    while True:
        try:
            readable, _, _ = select.select(inputs, [], [])
            for readable_sock in readable:
                if readable_sock is sys.stdin:
                    message = sys.stdin.readline().strip()
                    requestDict = inputParser.parseInput(message)
                    communicateManager.sendDict(requestDict, server_addr)
                else:
                    responseDict, addr = communicateManager.recvDict()
                    receipt = receiptManager.createReceipt(responseDict)
                    receipt.response()
        except Exception as e:
            logging.exception(e)
            
        print("> ", end="")
        sys.stdout.flush()
    systemEXIT()