from common.Singleton import singleton
from server.Corner import Corner
from server.User import User
import common.Utils as Utils

@singleton
class Receiver:
    def __init__(self):
        self.corners = {}
        self.users = {}
        self.admins = {}

    def addAdmin(self, ip, port):
        id = self.getAvailableUserId()
        user = User(id, ip, port)
        self.admins[id] = user
        return id

    def addUser(self, ip, port):
        id = self.getAvailableUserId()
        user = User(id, ip, port)
        self.users[id] = user
        return id

    def removeAdmin(self, userId):
        if userId in self.admins:
            return
        del self.admins[userId]

    def removeUser(self, userId):
        if userId in self.users:
            return
        del self.users[userId]

    def addCorner(self, cornerName, cornerLanguage):
        if cornerName in self.corners:
            return
        corner = Corner(cornerName, cornerLanguage)
        self.corners[cornerName] = corner

    def removeCorner(self, cornerName):
        if cornerName not in self.corners:
            return
        del self.corners[cornerName]

    def getCornerByCornerName(self, cornerName):
        if cornerName not in self.corners:
            return None
        return self.corners[cornerName]

    def getAdminByUserId(self, userId):
        if userId not in self.admins:
            return None
        return self.admins[userId]

    def getUserByUserId(self, userId):
        if userId not in self.users:
            return None
        return self.users[userId]

    def getAllCorners(self):
        return self.corners

    def getAllUsers(self):
        return self.users

    def getAllUsersOfCurrentCorner(self, userId):
        user = None
        if userId in self.users:
            user = self.users[userId]
        else:
            user = self.admins[userId]
        if user.cornerIn is None:
            return None
        else:
            return user.cornerIn.users

    def getAvailableUserId(self):
        randomId = Utils.getRandomUserId()
        while randomId in self.users or randomId in self.admins:
            randomId = Utils.getRandomUserId()
        return randomId

    def action(self, cmdStr):
        return f"Receiver get command {cmdStr}"

    