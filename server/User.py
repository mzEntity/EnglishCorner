class User:
    def __init__(self, id, ip, port):
        self.id = id
        self.ip = ip
        self.port = port
        self.cornerIn = {}


    def sendMessage(self, message):
        # TODO
        pass

    def joinCorner(self, corner):
        self.cornerIn[corner.name] = corner

    def leaveCorner(self, cornerName):
        if cornerName not in self.cornerIn:
            return
        del self.cornerIn[cornerName]