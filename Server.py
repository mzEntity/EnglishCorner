
import logging
from common.Config import *
from common.Protocol import ProtocolTranslator
from common.workspace.CommandFactory import CommandFactory
from server.Background import Background
from common.SocketUtils import SocketManager

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


if __name__ == "__main__":
    # 创建UDP Socket

    socketManager = SocketManager()
    # 绑定Socket到本地IP地址和端口号
    socketManager.bind(server_addr)

    # 接收数据
    while True:
        data, addr = socketManager.recv()
        msg = data.decode("utf-8")

        print("received message from", addr)
        if msg == "bye":
            break
        # 发送回复消息
        reply_message = responseToMsg(msg, addr)
        socketManager.sendTo(reply_message.encode("utf-8"), addr)

    socketManager.close()