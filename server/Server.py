import socket

from common.Config import *
from common.Protocol import ProtocolTranslator
from common.workspace.CommandFactory import CommandFactory
from server.Background import Background
from common.workspace.ReceiptManager import ReceiptManager

def responseToMsg(msg):
    translator = ProtocolTranslator()
    cmdFactory = CommandFactory()
    background = Background()
    receiptManager = ReceiptManager()

    msgDict = translator.strToDict(msg)
    cmd = cmdFactory.createCommand(msgDict)
    receipt = background.executeCommand(cmd)
    receiptDict = receiptManager.parseReceipt(receipt)
    returnMsg = translator.dictToStr(receiptDict)
    return returnMsg



# 创建UDP Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定Socket到本地IP地址和端口号
sock.bind(server_addr)

# 接收数据
while True:
    data, addr = sock.recvfrom(1024)
    msg = data.decode("utf-8")
    print("received message from", addr)
    if msg == "quit":
        break
    # 发送回复消息
    reply_message = responseToMsg(msg)
    sock.sendto(reply_message.encode("utf-8"), addr)
