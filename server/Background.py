from common.Singleton import singleton
from common.workspace.ReceiptManager import ReceiptManager

@singleton
class Background:
    def __init__(self):
        self.receiptManager = ReceiptManager()

    def executeCommand(self, command):
        result = command.execute()
        return self.receiptManager.createReturnDict(command.type, result)
        


