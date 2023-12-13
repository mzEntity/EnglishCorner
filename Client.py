from common.Config import *
from client.InputParser import InputParser
from common.Cache import GlobalCache
from common.workspace.ReceiptManager import ReceiptManager
from common.SocketUtils import CommunicateManager
from common.Utils import *
import select
from common.ConsoleManager import ConsoleManager



if __name__ == "__main__":
    GlobalCache().setUserInfo("id", "")
    GlobalCache().setUserInfo("role", "visitor")
    inputParser = InputParser()
    communicateManager = CommunicateManager()
    receiptManager = ReceiptManager()
    
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
            ConsoleManager().print(e)
            
        sys.stdout.flush()