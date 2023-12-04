from server.Receiver import Receiver
from common.workspace.ReceiptManager import ReceiptManager

class Command:
    def __init__(self, headerDict, bodyStr):
        self.type = headerDict["type"]
        self.body = bodyStr
        self.receiver = Receiver()
        self.receiptManager = ReceiptManager()

    def execute(self):
        pass


class CornersCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def execute(self):
        result = self.receiver.action(self.type)
        receipt = self.receiptManager.createReceipt(self.type, result)
        return receipt

    @staticmethod
    def createDict(elements):
        if len(elements) != 1:
            raise InvalidCommandException("Invalid /corners command")
        cmd_dict = {
            "header": {
                "mode": "command",
                "type": "corners"
            },
            "body": "EMPTY"
        }
        return cmd_dict

    
class ListusersCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def execute(self):
        result = self.receiver.action(self.type)
        receipt = self.receiptManager.createReceipt(self.type, result)
        return receipt

    @staticmethod
    def createDict(elements):
        if len(elements) != 1:
            raise InvalidCommandException("Invalid /listusers command")
        cmd_dict = {
            "header": {
                "mode": "command",
                "type": "listusers"
            },
            "body": "EMPTY"
        }
        return cmd_dict


class HeaderLackOfMemberException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class InvalidCommandException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message
