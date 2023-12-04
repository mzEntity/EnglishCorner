from common.workspace.CommandFactory import CommandFactory
from common.Singleton import singleton

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
            requestDict = self.commandFactory.createDict(requestType, elements)
            return requestDict
        except Exception as e:
            raise InvalidRequestException(str(e))

class InvalidRequestException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message
