from common.workspace.Receipt import *
from common.Singleton import singleton

@singleton
class ReceiptManager:
    def __init__(self):
        self.validReceipt = {
            "corners": CornersReceipt, 
            "listusers": ListusersReceipt
        }

    def createReceipt(self, receiptType, result):
        if receiptType not in self.validReceipt:
            raise InvalidReceiptException("createReceipt: no such receipt")
        newReceipt = self.validReceipt[receiptType](result)
        return newReceipt

    def parseReceipt(self, receipt):
        return receipt.getDict()