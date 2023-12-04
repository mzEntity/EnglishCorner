from common.workspace.CommandFactory import CommandFactory
from common.Singleton import singleton
from common.Cache import GlobalCache

@singleton
class InputParser:
    def __init__(self):
        self.commandFactory = CommandFactory()

    def parseInput(self, inputStr):
        elements = inputStr.split(" ")
        try:
            requestDict = self._getRequestDict(elements)
            return requestDict
        except InvalidRequestException as e:
            raise e

    def _getRequestDict(self, elements):
        if len(elements) < 1:
            raise InvalidRequestException("_getRequestDict: Invalid request")
        requestType = elements[0]
        try:
            headerDict = {
                "type": requestType,
                "user": GlobalCache().getUserInfo("id"),
            }
            bodyStr = self.commandFactory.createBodyStr(elements)
            requestDict = {
                "header": headerDict,
                "body": bodyStr
            }
            return requestDict
        except Exception as e:
            raise InvalidRequestException(str(e))

class InvalidRequestException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message
