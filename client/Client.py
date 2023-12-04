import socket

from common.Config import *
from client.InputParser import InputParser
from common.Protocol import ProtocolTranslator



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
        print(str(e))
        return None
    
def waitForInput():
    print(">", end="")
    message = input()
    return message

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
    print(data.decode("utf-8"))

# 关闭Socket连接
sock.close()
