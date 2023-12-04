from server.Receiver import Receiver



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
        if self.body == "root":
            return self.receiver.addAdmin(self.ip, self.port)
        elif self.body == "client":
            return self.receiver.addUser(self.ip, self.port)
        else:
            return None

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
        return cornerList

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
        userList = []
        if users is None:
            userList = None
        else:
            for userId in users.keys():
                userList.append(userId)
        return userList

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
        return self.receiver.addCorner(self.cornerName, self.cornerLanguage)

    @staticmethod
    def createBodyStr(elements):
        if len(elements) != 3 or elements[0] != "opencorner":
            raise InvalidCommandException("Invalid /opencorner command")
        return elements[1] + "\t" + elements[2]

class InvalidCommandException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message
