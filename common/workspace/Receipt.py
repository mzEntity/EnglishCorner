class Receipt:
    def __init__(self, content=""):
        self.content = content


class CornersReceipt(Receipt):

    def __init__(self, result):
        super().__init__(result)
    
    def getDict(self):
        receiptDict = {
            "header": {
                "mode": "command",
                "type": "corners",
                "state": "success"
            },
            "body": self.content
        }
        return receiptDict

class ListusersReceipt(Receipt):

    def __init__(self, result):
        super().__init__(result)

    def getDict(self):
        receiptDict = {
            "header": {
                "mode": "command",
                "type": "listusers",
                "state": "success"
            },
            "body": self.content
        }
        return receiptDict


class InvalidReceiptException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message