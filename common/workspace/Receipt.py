from common.Cache import GlobalCache

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
            userId = self.body
            print(f"login: {userId}")
            GlobalCache().setUserInfo("id", userId)
        else:
            print(self.msg)

    @staticmethod
    def getDict(result):
        bodyStr = result
        if bodyStr is None:
            return createFailReceiptDict("login", "Invalid mode", "")
        return createSuccessReceiptDict(
            "login", "login success", bodyStr)

class CornersReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)
    

    def response(self):
        if self.code != "200":
            print(self.msg)
            return
        bodyStr = self.body
        cornerList = bodyStr.split("\n")
        print("%10s|%10s" % ("name", "language"))
        for corner in cornerList:
            cornerName, language = corner.split("\t")
            print("%10s %10s" % (cornerName, language))
            

    @staticmethod
    def getDict(result):
        bodyStr = ""
        if len(result) != 0:
            firstCorner = result[0]
            bodyStr = firstCorner.name + "\t" + firstCorner.language
            for corner in result[1:]:
                bodyStr += "\n" + corner.name + "\t" + corner.language
        return createSuccessReceiptDict(
            "corners", "list all corners", bodyStr)
        

class ListusersReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        if self.code != "200":
            print(self.msg)
            return
        bodyStr = self.body
        userList = bodyStr.split("\n")
        print("users: ")
        for userName in userList:
            print(userName)


    @staticmethod
    def getDict(result):
        type = "listusers"
        if result is None:
            msg = "You are not in any corner"
            return createFailReceiptDict(type, msg, "")
        msg = "list all users"
        bodyStr = ""
        if len(result) != 0:
            firstUser = result[0]
            bodyStr = firstUser.name
            for user in result[1:]:
                bodyStr += "\n" + user.name
        return createSuccessReceiptDict(type, msg, bodyStr)

class OpenCornerReceipt(Receipt):

    def __init__(self, headerDict, bodyStr):
        super().__init__(headerDict, bodyStr)

    def response(self):
        print(self.msg)

    @staticmethod
    def getDict(result):
        type = "opencorner"
        if not result:
            msg = "cornerName already exists"
            return createFailReceiptDict(type, msg, "")
        msg = "open corner success"
        return createSuccessReceiptDict(type, msg, "")




def createHeaderDict(type, code, msg):
    headerDict = {
        "type": type,
        "code": code,
        "msg": msg
    }
    return headerDict

def createSuccessHeaderDict(type, msg):
    return createHeaderDict(type, "200", msg)

def createFailHeaderDict(type, msg):
    return createHeaderDict(type, "400", msg)

def createReceiptDict(header, body):
    receiptDict = {
        "header": header,
        "body": body
    }
    return receiptDict

def createSuccessReceiptDict(type, msg, body):
    return createReceiptDict(createSuccessHeaderDict(type, msg), body)

def createFailReceiptDict(type, msg, body):
    return createReceiptDict(createFailHeaderDict(type, msg), body)