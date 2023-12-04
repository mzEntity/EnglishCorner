class User:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.cornerIn = None

    def sendMessage(self, message):
        # TODO
        pass

    def joinCorner(self, corner):
        self.cornerIn = corner

    def leaveCorner(self):
        self.cornerIn = None

    def getCorner(self):
        return self.cornerIn