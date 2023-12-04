from common.workspace.Receipt import *
from common.Singleton import singleton

@singleton
class ReceiptManager:
    def __init__(self):
        self.validReceipt = {
            "login": LoginReceipt,
            "corners": CornersReceipt, 
            "listusers": ListusersReceipt,
            "opencorner": OpenCornerReceipt
        }

    def createReceiptDict(self, receiptType, result):
        if receiptType not in self.validReceipt:
            raise InvalidReceiptException("createReceipt: no such receipt")
        return self.validReceipt[receiptType].getDict(result)

    def parseReceipt(self, receipt):
        return receipt.getDict()