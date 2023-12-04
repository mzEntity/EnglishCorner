from server.User import User

class Corner:
    def __init__(self, cornerName, cornerLanguage):
        self.name = cornerName
        self.language = cornerLanguage
        self.users = {}
        self.admins = {}

    def addAdmin(self, user):
        userId = user.id
        self.admins.setdefault(userId, user)

    def addUser(self, user):
        userId = user.id
        self.users.setdefault(userId, user)
        self.sendSystemINFO(f"Welcome user {user.id}")

    def removeUser(self, userId):
        if userId not in self.users:
            return
        user = self.users[userId]
        del self.users[userId]
        self.sendSystemINFO(f"goodbye user {user.id}")

    def sendMessage(self, fromUserId, msg):
        for userId, user in self.users.items():
            if userId == fromUserId:
                continue
            user.sendMessage(msg)
    
    def sendSystemINFO(self, msg):
        for _, user in self.users.items():
            user.sendMessage(msg)

    def close(self):
        self.sendSystemINFO(f"Corner {self.name} closed.")
        self.users.clear()
