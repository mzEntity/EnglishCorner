class HeaderDict:
    def __init__(self, dic={}):
        self._dic = {}
        for key, val in dic.items():
            if isinstance(key, str) and isinstance(val, str):
                self._dic[key] = val
        
    def __getitem__(self, key):
        return self._dic[key]

    def __setitem__(self, key, val):
        if isinstance(key, str):
            if isinstance(val, str):
                self._dic[key] = val
            else:
                print("Warning[HeaderDict]: Value has to be str type")
        else:
            print("Warning[HeaderDict]: Key has to be str type")

    def __contains__(self, key):
        return self._dic.__contains__(key)


class MessageDict:
    def __init__(self, headerDict=None, bodyStr=""):
        if isinstance(headerDict, HeaderDict):
            self.header = headerDict
        elif isinstance(headerDict, dict):
            self.header = HeaderDict(dict)
        else:
            self.header = HeaderDict()
        self.body = bodyStr

    def __getitem__(self, key):
        if key == "header":
            return self.header
        elif key == "body":
            return self.body
        else:
            return None

    def __setitem__(self, key, val):
        if key == "header":
            if isinstance(val, HeaderDict):
                self.header = val
            elif isinstance(val, dict):
                self.header = HeaderDict(val)
        elif key == "body":
            if isinstance(val, str):
                self.body = val

