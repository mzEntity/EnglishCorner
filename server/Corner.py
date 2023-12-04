from server.User import User

class Corner:
    def __init__(self, cornerName, cornerLanguage):
        self.name = cornerName
        self.language = cornerLanguage
        self.users = {}
        self.admins = {}
        self.idNamePair = {}

    def addAdmin(self, user):
        self.admins[user.id] = user

    def addUser(self, user, userName):
        self.users[userName] = user
        self.idNamePair[user.id] = userName

    def removeAdmin(self, userId):
        if userId not in self.admins:
            return
        del self.admins[userId]

    def removeUser(self, userId):
        if userId not in self.idNamePair:
            return
        userName = self.idNamePair[userId]
        del self.users[userName]
        del self.idNamePair[userId]

    def containAdmin(self, adminId):
        return adminId in self.admins

    def containUserName(self, userName):
        return userName in self.users

    def containUserId(self, userId):
        return userId in self.idNamePair

    def getUsers(self):
        return self.users
    
    def getAdmins(self):
        return self.admins

    def close(self):
        self.users.clear()
        self.admins.clear()

    
