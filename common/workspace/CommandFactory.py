from common.workspace.Command import *
from common.Singleton import singleton

@singleton
class CommandFactory:
    
    def __init__(self):
        self.validCommand = {
            "login": LoginCommand,
            "corners": CornersCommand, 
            "listusers": ListusersCommand,
            "opencorner": OpenCornerCommand
        }

    def createCommand(self, commandDict):
        headerDict = commandDict["header"]
        if "type" not in headerDict:
            raise HeaderLackOfMemberException("createCommand: type")
        if "user" not in headerDict:
            raise HeaderLackOfMemberException("createCommand: user")
        commandType = headerDict["type"]
        if commandType not in self.validCommand:
            raise InvalidCommandException("createCommand: no such command")
        newCommand = self.validCommand[commandType](headerDict, commandDict["body"])
        return newCommand

    def createBodyStr(self, elements):
        requestType = elements[0]
        if requestType not in self.validCommand:
            raise InvalidCommandException("createDict: No such requestType")
        return self.validCommand[requestType].createBodyStr(elements)
        

class HeaderLackOfMemberException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message