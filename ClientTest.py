from common.Config import *
from client.InputParser import InputParser
from common.Cache import GlobalCache
from common.workspace.ReceiptManager import ReceiptManager
from common.SocketUtils import CommunicateManager
from common.Utils import *
import time
import select
import re

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
    
    testFileName = sys.argv[1]
    testLines = processTest(getTest(testFileName))
    
    index = 0
    while True:
        try:
            time.sleep(0.1)
            if index < len(testLines):
                message = testLines[index].strip()
                index += 1
                requestDict = inputParser.parseInput(message)
                communicateManager.sendDict(requestDict, server_addr)
            readable, _, _ = select.select([sock], [], [])
            for readable_sock in readable:
                responseDict, addr = communicateManager.recvDict()
                receipt = receiptManager.createReceipt(responseDict)
                receipt.response()
        except Exception as e:
            print(e)
        sys.stdout.flush()
        