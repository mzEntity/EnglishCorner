from common.workspace.Command import *
from common.Singleton import singleton
from common.exception.Exceptions import *

@singleton
class CommandFactory:
    def __init__(self):
        rootCommand = {
            "corners": CornersCommand, 
            "listusers": ListusersCommand,
            "opencorner": OpenCornerCommand,
            "enter": EnterCommand,
            "exit": ExitCommand,
            "kickout": KickOutCommand,
            "closecorner": CloseCornerCommand,
            "leave": LeaveCommand
        }
        
        clientCommand = {
            "corners": CornersCommand, 
            "listusers": ListusersCommand,
            "join": JoinCommand,
            "quit": QuitCommand,
            "private": PrivateCommand,
            "msg": MsgCommand,
            "leave": LeaveCommand
        }
        
        visitorCommand = {
            "login": LoginCommand,
            "corners": CornersCommand, 
            "leave": LeaveCommand
        }
        
        self.validCommand = {}
        self.validCommand.update(rootCommand)
        self.validCommand.update(clientCommand)
        self.validCommand.update(visitorCommand)
        
        self.commandDict = {
            "root": rootCommand, 
            "client": clientCommand,
            "visitor": visitorCommand
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

    def createBodyStr(self, role, elements):
        requestType = elements[0]
        if role not in self.commandDict:
            raise InvalidCommandException("No such role.")
        if requestType not in self.commandDict[role]:
            raise InvalidCommandException("createDict: No such requestType")
        return self.validCommand[requestType].createBodyStr(elements)
        

