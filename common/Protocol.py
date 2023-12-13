"""
Translator类，将dict和str互相转化
"""

import re

from common.MessageDict import MessageDict
from common.Singleton import singleton
from common.exception.Exceptions import *


@singleton
class ProtocolTranslator:
    """
    translate UDP message to dict\n
    translate dict to UDP message
    """
    def __init__(self):
        self.packetManager = _PacketManager()
        self.headerManager = _HeaderManager()
    
    def strToDict(self, packetStr):
        """
        InvalidPacketException\n
        InvalidHeaderException
        """
        msgDict = MessageDict()
        try:
            headerStr, bodyStr = self.packetManager.splitPacket(packetStr)
            headerDict = self.headerManager.parseHeader(headerStr)
            msgDict["header"] = headerDict
            msgDict["body"] = bodyStr

            return msgDict
        except InvalidPacketException as e:
            raise e
        except InvalidHeaderException as e:
            raise e

    def dictToStr(self, msgDict):
        headerDict = msgDict["header"]
        bodyStr = msgDict["body"]
        headerStr = self.headerManager.generateHeader(headerDict)
        packetStr = self.packetManager.generatePacket(headerStr, bodyStr)
        return packetStr


class _PacketManager:

    def __init__(self):
        pass

    def generatePacket(self, headerStr, bodyStr):
        """
        join header and body\n
        return packetStr: str\n
        """
        return headerStr + bodyStr

    def splitPacket(self, packetStr):
        """
        separate packet into header and body\n
        raise InvalidPacketException\n
        return header: str, body: str\n
        """
        regex = r"\r\n\r\n"
        match = re.search(regex, packetStr)
        if not match:
            raise InvalidPacketException("splitPacket: Invalid packetStr")
        result = packetStr.split(match.group(), 1)
        if len(result) < 2:
            raise InvalidPacketException("splitPacket: Invalid packetStr")
        headerStr = result[0] + "\r\n\r\n"
        bodyStr = result[1]
        return headerStr, bodyStr

    
class _HeaderManager:

    def __init__(self):
        pass

    def parseHeader(self, headerStr):
        """
        InvalidHeaderException
        """
        header_dict = {}
        try:
            lines = self._getHeaderLines(headerStr)
            for line in lines:
                key, val = self._separateKeyVal(line)
                header_dict[key] = val
            return header_dict
        except InvalidHeaderException as e:
            raise e

    def generateHeader(self, headerDict):
        """
        translate dict to headerStr\n
        return header: str\n
        """
        header = ""
        for key, item in headerDict.items():
            escapedKey = key.replace(":", "\\:")
            escapedItem = item.replace(":", "\\:")
            line = escapedKey + ": " + escapedItem + "\r\n"
            header += line
        header += "\r\n"
        return header

    def _getHeaderLines(self, headerStr):
        """
        separate header into lines\n
        raise InvalidHeaderException\n
        return lines: List\n
        """
        lines = headerStr.split("\r\n")
        if len(lines) < 2:
            raise InvalidHeaderException("_getHeaderLines: Invalid headerStr")
        if lines[-1] != "" or lines[-2] != "":
            raise InvalidHeaderException("_getHeaderLines: Invalid headerStr")
        lines.pop()
        lines.pop()
        return lines

    def _separateKeyVal(self, headerLine):
        """
        separate key-val pair in one line\n
        raise InvalidHeaderException\n
        return (key: str, val: str)\n
        """
        pattern = r"(?<!\\): "
        result = re.split(pattern, headerLine)
        if len(result) != 2:
            raise InvalidHeaderException("_separateKeyVal: Invalid headerLine")
        key = result[0].replace("\\:", ":")
        val = result[1].replace("\\:", ":")
        return (key, val)







if __name__ == "__main__":
    pass