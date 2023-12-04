import socket
import logging
from common.Config import *
from common.Protocol import ProtocolTranslator
from common.workspace.CommandFactory import CommandFactory
from server.Background import Background

def setAddrToHeader(msgDict, addr):
    msgDict["header"]["ip"] = addr[0]
    msgDict["header"]["port"] = str(addr[1])

def responseToMsg(msg, addr):
    translator = ProtocolTranslator()
    cmdFactory = CommandFactory()
    background = Background()
    try:
        msgDict = translator.strToDict(msg)
        setAddrToHeader(msgDict, addr)
        cmd = cmdFactory.createCommand(msgDict)
        receiptDict = background.executeCommand(cmd)
        returnMsg = translator.dictToStr(receiptDict)
        return returnMsg
    except Exception as e:
        logging.exception(e)
        return ""

    

# 创建UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定Socket到本地IP地址和端口号
sock.bind(server_addr)

# 接收数据
while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode("utf-8")
    print("received message from", addr)
    if msg == "bye":
        break
    # 发送回复消息
    reply_message = responseToMsg(msg, addr)
    sock.sendto(reply_message.encode("utf-8"), addr)
