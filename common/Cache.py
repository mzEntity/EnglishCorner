from common.Singleton import singleton

@singleton
class GlobalCache:
    def __init__(self):
        self.userInfo = {}

    def setUserInfo(self, key, val):
        self.userInfo[key] = val

    def getUserInfo(self, key):
        if key not in self.userInfo:
            return None
        return self.userInfo[key]