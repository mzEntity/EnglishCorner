from common.Cache import GlobalCache
from common.Utils import *

class Receipt:
    def __init__(self, headerDict, bodyStr):
        self.type = headerDict["type"]
        self.code = headerDict["code"]
        self.msg = headerDict["msg"]
        self.body = bodyStr

    def response(self):
        pass

class LoginReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        if self.code == "200":
            role, userId = self.body.split("\t")
            print(f"login: {userId}({role})")
            GlobalCache().setUserInfo("id", userId)
            GlobalCache().setUserInfo("role", role)
        else:
            print(self.msg)

        

class CornersReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
    

    def response(self):
        if self.code != "200":
            print(self.msg)
            return
        bodyStr = self.body
        if bodyStr == "":
            print("There is no corner.")
            return
        cornerList = bodyStr.split("\n")
        print("%10s %10s" % ("name", "language"))
        for corner in cornerList:
            cornerName, language = corner.split("\t")
            print("%10s %10s" % (cornerName, language))
            

    
class ListusersReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        if self.code != "200":
            print(self.msg)
            return
        bodyStr = self.body
        if bodyStr == "":
            print("There is no user.")
            return
        userList = bodyStr.split("\n")
        print("%10s|%10s" % ("username", "userid"))
        for user in userList:
            userName, userId = user.split("\t")
            print("%10s %10s" % (userName, userId))

        

class OpenCornerReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)
        
class EnterReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)

class ExitReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)

class CloseCornerReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)

class LeaveReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)
        systemEXIT()

class JoinReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)

class QuitReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)
        
class PrivateReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)
        
class PrivateReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)
        
class WhisperReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        fromId, content = self.body.split("\t")
        print(f"[PRIVATE]{fromId}: {content}")
        
        
class MsgReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)
        
        
class ChatReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        cornerName, fromName, content = self.body.split("\t")
        print(f"[{cornerName}]{fromName}: {content}")
        
class KickOutReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)
        
class SystemReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        content = self.body
        print(f"[SYSTEM]: {content}")