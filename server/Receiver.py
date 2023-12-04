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
        user.sendMessage("Hello")
        self.admins.setdefault(id, user)
        return id

    def addUser(self, ip, port):
        id = self.getAvailableUserId()
        user = User(id, ip, port)
        user.sendMessage("Hello")
        self.users.setdefault(id, user)
        return id

    def addCorner(self, cornerName, cornerLanguage):
        if cornerName in self.corners:
            return False
        corner = Corner(cornerName, cornerLanguage)
        self.corners[cornerName] = corner
        return True

    def removeUser(self, userId):
        if userId not in self.users:
            return
        user = self.users[userId]
        if user.cornerIn is None:
            return
        user.cornerIn.removeUser(userId)
        user.sendMessage("GoodBye")
        del self.users[userId]
    
    def removeCorner(self, cornerName):
        if cornerName not in self.corners:
            return
        corner = self.corners[cornerName]
        usersInCorner = corner.users
        for _, user in usersInCorner.items():
            user.leaveCorner()
        corner.close()
        del self.corners[cornerName]

    def getCornerByCornerName(self, cornerName):
        if cornerName not in self.corners:
            return None
        return self.corners[cornerName]
        

    def userJoinCorner(self, userId, cornerName):
        if userId not in self.users or cornerName not in self.corners:
            return
        user = self.users[userId]
        corner = self.corners[cornerName]
        user.joinCorner(corner)
        corner.addUser(user)

    def userLeaveCorner(self, userId, cornerName):
        if userId not in self.users or cornerName not in self.corners:
            return
        user = self.users[userId]
        corner = self.corners[cornerName]
        user.leaveCorner()
        corner.removeUser(user)

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

    