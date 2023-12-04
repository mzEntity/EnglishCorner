from server.Receiver import Receiver

from common.exception.Exceptions import *
from server.Corner import Corner

class Command:
    def __init__(self, headerDict, bodyStr):
        self.type = headerDict["type"]
        self.userId = headerDict["user"]
        self.ip = headerDict["ip"]
        self.port = headerDict["port"]
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

        return createSuccessReceiptDict(self.type, "login success", userId)

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
        for _, user in users.items():
            bodyStr += user.name + "\n"
            
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
        for _, user in users.items():
            user.leaveCorner()
        for _, admin in admins.items():
            admin.leaveCorner()
        corner.close()
        return createSuccessReceiptDict(self.type, "close corner successfully", "")
        
    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 2 or elements[0] != "closecorner":
            raise InvalidCommandException("Invalid /closecorner command")
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