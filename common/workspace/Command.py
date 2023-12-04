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
        cornerList = []
        for _, corner in corners.items():
            cornerList.append(corner)
        bodyStr = ""
        if len(cornerList) != 0:
            firstCorner = cornerList[0]
            bodyStr = firstCorner.name + "\t" + firstCorner.language
            for corner in cornerList[1:]:
                bodyStr += "\n" + corner.name + "\t" + corner.language
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

        userList = []
        for userId in users.keys():
            userList.append(userId)
            
        msg = "list all users"
        bodyStr = ""
        if len(userList) != 0:
            firstUser = userList[0]
            bodyStr = firstUser.name
            for user in userList[1:]:
                bodyStr += "\n" + user.name
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
        if not self.receiver.addCorner(self.cornerName, self.cornerLanguage):
            msg = "cornerName already exists"
            return createFailReceiptDict(self.type, msg, "")
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
        corner.addAdmin(admin)
        admin.joinCorner(corner)
        return createSuccessReceiptDict(self.type, "enter corner successfully", "")

    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 2 or elements[0] != "enter":
            raise InvalidCommandException("Invalid /enter command")
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