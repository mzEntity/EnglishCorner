
import socket
import logging
from common.Protocol import ProtocolTranslator
from common.Config import *
from client.InputParser import InputParser
from common.Cache import GlobalCache

def translateToPacket(message):
    translator = ProtocolTranslator()
    inputParser = InputParser()

    if message == "quit":
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
        msgDict = translator.strToDict(msg)
        print(msgDict["header"]["msg"])
        print(msgDict["body"])
        if msgDict["header"]["type"] == 'login':
            id = msgDict["body"]
            GlobalCache().setUserInfo("id", id)
    except Exception as e:
        logging.exception(e)
    return 


GlobalCache().setUserInfo("id", "")
# 创建UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = waitForInput()

    packetStr = translateToPacket(message)

    if packetStr is None:
        continue

    sock.sendto(packetStr.encode("utf-8"), server_addr)

    if message == "quit":
        break

    data, addr = sock.recvfrom(1024)
    msg = data.decode("utf-8")
    responseToReceipt(msg)

# 关闭Socket连接
sock.close()
