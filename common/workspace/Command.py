from server.Receiver import Receiver

from common.exception.Exceptions import *


class Command:
    def __init__(self, headerDict, bodyStr):
        self.type = headerDict["type"]
        self.userId = headerDict["user"]
        self.ip = headerDict["ip"]
        self.port = int(headerDict["port"])
        self.body = bodyStr
        self.receiver = Receiver()

    def execute(self):
        pass

class LoginCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def execute(self):
        userId = None
        if self.body == "root":
            userId = self.receiver.addAdmin(self.ip, self.port)
        elif self.body == "client":
            userId = self.receiver.addUser(self.ip, self.port)

        if userId is None:
            return createFailReceiptDict(self.type, "Invalid mode", "")

        return createSuccessReceiptDict(self.type, "login success", self.body + "\t" + userId)

    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 2 or elements[0] != "login":
            raise InvalidCommandException("Invalid /login command")
        return elements[1]

class CornersCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def execute(self):
        corners = self.receiver.getAllCorners()
        bodyStr = ""
        for _, corner in corners.items():
            bodyStr += corner.name + "\t" + corner.language + "\n"

        if corners:
            bodyStr = bodyStr[:-1]

        return createSuccessReceiptDict(self.type, "list all corners", bodyStr)

    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 1 or elements[0] != "corners":
            raise InvalidCommandException("Invalid /corners command")
        return ""

    
class ListusersCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def execute(self):
        userId = self.userId
        users = self.receiver.getAllUsersOfCurrentCorner(userId)
        
        if users is None:
            msg = "You are not in any corner"
            return createFailReceiptDict(self.type, msg, "")

        bodyStr = ""
        for userName, user in users.items():
            bodyStr += userName + "\t" + user.id + "\n"
            
        msg = "list all users"
        
        if users:
            bodyStr = bodyStr[:-1]
                
        return createSuccessReceiptDict(self.type, msg, bodyStr)

    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 1 or elements[0] != "listusers":
            raise InvalidCommandException("Invalid /listusers command")
        return ""

class OpenCornerCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.cornerName, self.cornerLanguage = bodyStr.split("\t")

    def execute(self):
        if self.receiver.getCornerByCornerName(self.cornerName):
            msg = "cornerName already exists"
            return createFailReceiptDict(self.type, msg, "")

        self.receiver.addCorner(self.cornerName, self.cornerLanguage)
        msg = "open corner success"
        return createSuccessReceiptDict(self.type, msg, "")

    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 3 or elements[0] != "opencorner":
            raise InvalidCommandException("Invalid /opencorner command")
        return elements[1] + "\t" + elements[2]


class EnterCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.cornerName = bodyStr

    def execute(self):
        corner = self.receiver.getCornerByCornerName(self.cornerName)
        if corner is None:
            return createFailReceiptDict(self.type, "No such corner", "")
        admin = self.receiver.getAdminByUserId(self.userId)
        if admin.getCorner():
            return createFailReceiptDict(self.type, "You are already in a corner.", "")
        corner.addAdmin(admin)
        admin.joinCorner(corner)
        return createSuccessReceiptDict(self.type, "enter corner successfully", "")

    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 2 or elements[0] != "enter":
            raise InvalidCommandException("Invalid /enter command")
        return elements[1]

class ExitCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.cornerName = bodyStr

    def execute(self):
        corner = self.receiver.getCornerByCornerName(self.cornerName)
        if corner is None:
            return createFailReceiptDict(self.type, "No such corner", "")
        if not corner.containAdmin(self.userId):
            return createFailReceiptDict(self.type, "You are not in that corner", "")
        corner.removeAdmin(self.userId)
        admin = self.receiver.getAdminByUserId(self.userId)
        admin.leaveCorner()
        msg = "exit corner successfully"
        return createSuccessReceiptDict(self.type, msg, "")

    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 2 or elements[0] != "exit":
            raise InvalidCommandException("Invalid /exit command")
        return elements[1]


class CloseCornerCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.cornerName = bodyStr

    def execute(self):
        corner = self.receiver.getCornerByCornerName(self.cornerName)
        if corner is None:
            return createFailReceiptDict(self.type, "No such corner", "")
        users = corner.getUsers()
        admins = corner.getAdmins()
        corner.sendSystemMessage(f"{corner.name} is closed by admin.")
        for _, user in users.items():
            user.leaveCorner()
        for _, admin in admins.items():
            admin.leaveCorner()
        corner.close()
        self.receiver.removeCorner(corner.name)
        return createSuccessReceiptDict(self.type, "close corner successfully", "")
        
    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 2 or elements[0] != "closecorner":
            raise InvalidCommandException("Invalid /closecorner command")
        return elements[1]

class LeaveCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def execute(self):
        if self.userId == "":
            return createSuccessReceiptDict(self.type, "GoodBye.", "")
        user = self.receiver.getUserByUserId(self.userId)
        if user:
            corner = user.getCorner()
            if corner:
                user.leaveCorner()
                corner.removeUser(self.userId)
            self.receiver.removeUser(self.userId)
        else:
            admin = self.receiver.getAdminByUserId(self.userId)
            corner = admin.getCorner()
            if corner:
                admin.leaveCorner()
                corner.removeAdmin(self.userId)
            self.receiver.removeAdmin(self.userId)
        return createSuccessReceiptDict(self.type, "GoodBye.", "")
        
    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 1 or elements[0] != "leave":
            raise InvalidCommandException("Invalid /leave command")
        return ""

class JoinCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.cornerName, self.userName = bodyStr.split("\t")

    def execute(self):
        corner = self.receiver.getCornerByCornerName(self.cornerName)
        if corner is None:
            return createFailReceiptDict(self.type, "No such corner", "")
        user = self.receiver.getUserByUserId(self.userId)
        if user.getCorner():
            return createFailReceiptDict(self.type, "You are already in a corner.", "")
        if corner.containUserName(self.userName):
            return createFailReceiptDict(self.type, "Username already exists.", "")
        corner.addUser(user, self.userName)
        user.joinCorner(corner)
        corner.sendSystemMessage(f"Welcome {self.userName} to {corner.name}.")
        return createSuccessReceiptDict(self.type, "join corner successfully", "")
        
    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 3 or elements[0] != "join":
            raise InvalidCommandException("Invalid /join command")
        return elements[1] + "\t" + elements[2]

class QuitCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.cornerName = bodyStr

    def execute(self):
        corner = self.receiver.getCornerByCornerName(self.cornerName)
        if corner is None:
            return createFailReceiptDict(self.type, "No such corner", "")
        if not corner.containUserId(self.userId):
            return createFailReceiptDict(self.type, "You are not in that corner", "")
        corner.sendSystemMessage(f"{self.userId} leaves the corner {corner.name}.")
        corner.removeUser(self.userId)
        user = self.receiver.getUserByUserId(self.userId)
        user.leaveCorner()
        msg = "quit corner successfully"
        return createSuccessReceiptDict(self.type, msg, "")
        
    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 2 or elements[0] != "quit":
            raise InvalidCommandException("Invalid /quit command")
        return elements[1]

class PrivateCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.targetUserId, self.content = bodyStr.split("\t")

    def execute(self):
        user = self.receiver.getUserByUserId(self.targetUserId)
        if user is None:
            return createFailReceiptDict(self.type, "No such user", "")
        
        user.sendWhisperMessage(self.userId, self.content)
    
        msg = "send message successfully"
        return createSuccessReceiptDict(self.type, msg, "")
        
    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 3 or elements[0] != "private":
            raise InvalidCommandException("Invalid /private command")
        return elements[1] + "\t" + elements[2]

class MsgCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.cornerName, self.content = bodyStr.split("\t")

    def execute(self):
        corner = self.receiver.getCornerByCornerName(self.cornerName)
        if corner is None:
            return createFailReceiptDict(self.type, "No such corner", "")
        if not corner.containUserId(self.userId):
            return createFailReceiptDict(self.type, "You are not in that corner", "")
        
        corner.sendChatMessage(self.userId, self.content)
        msg = "send message successfully"
        return createSuccessReceiptDict(self.type, msg, "")
        
    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 3 or elements[0] != "msg":
            raise InvalidCommandException("Invalid /msg command")
        return elements[1] + "\t" + elements[2]
    
class KickOutCommand(Command):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
        self.targetUserId = bodyStr

    def execute(self):
        user = self.receiver.getUserByUserId(self.targetUserId)
        
        if user is None:
            return createFailReceiptDict(self.type, "No such user", "")
        admin = self.receiver.getAdminByUserId(self.userId)
        corner = admin.getCorner()
        if corner is None:
            return createFailReceiptDict(self.type, "You are not in any corner", "")

        if not corner.containUserId(self.targetUserId):
            return createFailReceiptDict(self.type, "target user is not in that corner", "")
        
        userName = corner.getUserNameByUserId(self.targetUserId)
        corner.sendSystemMessage(f"{userName}({self.targetUserId}) is kicked out from {corner.name}")
        user.sendSystemMessage(f"You are kickedout from {corner.name}")
        corner.removeUser(self.targetUserId)
        user.leaveCorner()
        msg = "remove user successfully"
        return createSuccessReceiptDict(self.type, msg, "")
        
    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 2 or elements[0] != "kickout":
            raise InvalidCommandException("Invalid /kickout command")
        return elements[1]


def createHeaderDict(type, code, msg):
    headerDict = {
        "type": type,
        "code": code,
        "msg": msg
    }
    return headerDict

def createSuccessHeaderDict(type, msg):
    return createHeaderDict(type, "200", msg)

def createFailHeaderDict(type, msg):
    return createHeaderDict(type, "400", msg)

def createReceiptDict(header, body):
    receiptDict = {
        "header": header,
        "body": body
    }
    return receiptDict

def createSuccessReceiptDict(type, msg, body):
    return createReceiptDict(createSuccessHeaderDict(type, msg), body)

def createFailReceiptDict(type, msg, body):
    return createReceiptDict(createFailHeaderDict(type, msg), body)