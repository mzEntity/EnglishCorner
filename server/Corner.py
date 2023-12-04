from server.User import User

class Corner:
    def __init__(self, cornerName, cornerLanguage):
        self.name = cornerName
        self.language = cornerLanguage
        self.users = {}
        self.admins = {}

    def addAdmin(self, user):
        userId = user.id
        self.admins[userId] = user

    def addUser(self, user):
        userId = user.id
        self.users[userId] = user

    def removeUser(self, userId):
        if userId not in self.users:
            return
        del self.users[userId]

    def removeAdmin(self, userId):
        if userId not in self.admins:
            return
        del self.admins[userId]

    def containAdmin(self, adminId):
        return adminId in self.admins

    def containUser(self, userId):
        return userId in self.users

    def getUsers(self):
        return self.users
    
    def getAdmins(self):
        return self.admins

    def close(self):
        self.users.clear()
        self.admins.clear()

    
