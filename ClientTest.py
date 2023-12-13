from common.Config import *
from client.InputParser import InputParser
from common.Cache import GlobalCache
from common.workspace.ReceiptManager import ReceiptManager
from common.SocketUtils import CommunicateManager
from common.Utils import *
import time
import select
import re
from common.ConsoleManager import ConsoleManager

def getTest(fileName):
    with open(fileName, "r", encoding="utf-8") as f:
        content = f.readlines()
    return content


def generateRandom(pattern):
    count = int(pattern.group(1))
    return generateRandomStr(count)

def processTest(testLines):
    processedTestLines = []
    regex = r"{(\d+)}"
    for line in testLines:
        result = re.sub(regex, generateRandom, line)
        processedTestLines.append(result)
    return processedTestLines
        

if __name__ == "__main__":
    GlobalCache().setUserInfo("id", "")
    GlobalCache().setUserInfo("role", "visitor")
    inputParser = InputParser()
    communicateManager = CommunicateManager()
    receiptManager = ReceiptManager()
    
    sys.stdout.flush()
    
    sock = communicateManager.getSocket()
    
    enable = sys.argv[1]
    if enable == "-e":
        ConsoleManager().enableConsoleManager()
    else:
        ConsoleManager().disableConsoleManager()
        
    testFileName = sys.argv[2]
    testLines = processTest(getTest(testFileName))
    sleepTimer = None
    alertTime = 0
    index = 0
    communicateManager.setTimeOut(0.1)
    while True:
        try:
            if index < len(testLines):
                if sleepTimer is not None:
                    if time.time() - sleepTimer < alertTime:
                        continue
                    else:
                        sleepTimer = None
                        alertTime = 0
                message = testLines[index].strip()
                index += 1
                if message.startswith("SLEEP"):
                    sleepTime = int(message.split(" ")[1])
                    sleepTimer = time.time()
                    alertTime = sleepTime
                    continue
                requestDict = inputParser.parseInput(message)
                communicateManager.sendDict(requestDict, server_addr)
            
            responseDict, addr = communicateManager.recvDict()
            receipt = receiptManager.createReceipt(responseDict)
            receipt.response()
        except Exception as e:
            pass
        sys.stdout.flush()
        