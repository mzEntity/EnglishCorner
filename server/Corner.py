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

    def removeUser(self, userName):
        if userName not in self.users:
            return
        userId = self.users[userName].id
        del self.users[userName]
        del self.idNamePair[userId]

    def containAdmin(self, adminId):
        return adminId in self.admins

    def containUser(self, userName):
        return userName in self.users

    def getUsers(self):
        return self.users
    
    def getAdmins(self):
        return self.admins

    def close(self):
        self.users.clear()
        self.admins.clear()

    
