

import logging
from common.Protocol import ProtocolTranslator
from common.Config import *
from client.InputParser import InputParser
from common.Cache import GlobalCache
from common.workspace.ReceiptManager import ReceiptManager
from common.SocketUtils import SocketManager

def translateToPacket(message):
    translator = ProtocolTranslator()
    inputParser = InputParser()

    if message == "bye":
        return message

    try:
        requestDict = inputParser.parseInput(message)
        packetStr = translator.dictToStr(requestDict)
        return packetStr
    except Exception as e:
        logging.exception(e)
        return None
    
def waitForInput():
    print(">", end="")
    message = input()
    return message

def responseToReceipt(msg):
    try:
        translator = ProtocolTranslator()
        receiptManager = ReceiptManager()
        msgDict = translator.strToDict(msg)
        receipt = receiptManager.createReceipt(msgDict)
        receipt.response()
        
            
    except Exception as e:
        logging.exception(e)
    return 


GlobalCache().setUserInfo("id", "")

socketManager = SocketManager()

while True:
    message = waitForInput()

    packetStr = translateToPacket(message)

    if packetStr is None:
        continue

    socketManager.sendTo(packetStr.encode("utf-8"), server_addr)
    
    if message == "bye":
        break

    data, addr = socketManager.recv()

    msg = data.decode("utf-8")
    responseToReceipt(msg)

socketManager.close()
