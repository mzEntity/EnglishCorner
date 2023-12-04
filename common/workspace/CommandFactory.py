from common.workspace.Command import *
from common.Singleton import singleton

@singleton
class CommandFactory:
    
    def __init__(self):
        self.validCommand = {
            "corners": CornersCommand, 
            "listusers": ListusersCommand
        }

    def createCommand(self, commandDict):
        headerDict = commandDict["header"]
        if "mode" not in headerDict:
            raise HeaderLackOfMemberException("createCommand: mode")
        if headerDict["mode"] != "command":
            raise InvalidCommandException("createCommand: not in command mode")
        if "type" not in headerDict:
            raise HeaderLackOfMemberException("createCommand: type")
        commandType = headerDict["type"]
        if commandType not in self.validCommand:
            raise InvalidCommandException("createCommand: no such command")
        newCommand = self.validCommand[commandType](headerDict, commandDict["body"])
        return newCommand

    def createDict(self, requestType, elements):
        if requestType not in self.validCommand:
            raise InvalidCommandException("createDict: No such requestType")
        return self.validCommand[requestType].createDict(elements)
        