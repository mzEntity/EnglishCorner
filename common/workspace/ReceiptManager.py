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
            "opencorner": OpenCornerReceipt
        }

    def createReceipt(self, receiptDict):
        headerDict = receiptDict["header"]
        if "type" not in headerDict:
            raise HeaderLackOfMemberException("createCommand: type")
        if "user" not in headerDict:
            raise HeaderLackOfMemberException("createCommand: user")
        commandType = headerDict["type"]
        if commandType not in self.validCommand:
            raise InvalidCommandException("createCommand: no such command")
        newCommand = self.validCommand[commandType](headerDict, receiptDict["body"])
        return newCommand

    def createReturnDict(self, receiptType, result):
        if receiptType not in self.validReceipt:
            raise InvalidReceiptException("createReceipt: no such receipt")
        return self.validReceipt[receiptType].getDict(result)