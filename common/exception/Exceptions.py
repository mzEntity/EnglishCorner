class InvalidReceiptException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class InvalidCommandException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class HeaderLackOfMemberException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class InvalidRequestException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class InvalidPacketException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message

class InvalidHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message