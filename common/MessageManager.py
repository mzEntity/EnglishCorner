from common.Singleton import singleton

@singleton
class MessageManager:
    def __init__(self):
        pass
    
    def buildWhisperDict(self, fromId, content):
        headerDict = {
            "type": "whisper",
            "code": "200",
            "msg": "message from user"
        }
        body = fromId + "\t" + content
        return {
            "header": headerDict,
            "body": body
        }
        
    def buildSystemDict(self, content):
        headerDict = {
            "type": "system",
            "code": "200",
            "msg": "system message"
        }
        body = content
        return {
            "header": headerDict,
            "body": body
        }
    
    def buildChatDict(self, cornerName, userName, content):
        headerDict = {
            "type": "chat",
            "code": "200",
            "msg": "message in corner"
        }
        body = cornerName + "\t" + userName + "\t" + content
        return {
            "header": headerDict,
            "body": body
        }
        
    def buildOutOfDateDict(self):
        headerDict = {
            "type": "outofdate",
            "code": "200",
            "msg": "system message"
        }
        return {
            "header": headerDict,
            "body": ""
        }