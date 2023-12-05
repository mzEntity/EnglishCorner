from common.workspace.Receipt import *
from common.Singleton import singleton
from common.exception.Exceptions import *

@singleton
class ReceiptManager:
    def __init__(self):
        self.validReceipt = {
            "login": LoginReceipt,
            "corners": CornersReceipt, 
            "listusers": ListusersReceipt,
            "opencorner": OpenCornerReceipt,
            "enter": EnterReceipt,
            "exit": ExitReceipt,
            "closecorner": CloseCornerReceipt,
            "leave": LeaveReceipt,
            "join": JoinReceipt,
            "quit": QuitReceipt,
            "private": PrivateReceipt,
            "whisper": WhisperReceipt,
            "msg": MsgReceipt,
            "chat": ChatReceipt,
            "kickout": KickOutReceipt
        }

    def createReceipt(self, receiptDict):
        headerDict = receiptDict["header"]
        if "type" not in headerDict:
            raise HeaderLackOfMemberException("createReceipt: type")
        if "code" not in headerDict:
            raise HeaderLackOfMemberException("createReceipt: code")
        if "msg" not in headerDict:
            raise HeaderLackOfMemberException("createReceipt: msg")
        receiptType = headerDict["type"]
        if receiptType not in self.validReceipt:
            raise InvalidReceiptException("createReceipt: no such receipt")
        newReceipt = self.validReceipt[receiptType](headerDict, receiptDict["body"])
        return newReceipt