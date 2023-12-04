import random
from common.Config import *
import sys
from common.SocketUtils import CommunicateManager

def getRandomUserId():
    idLength = user_id_length
    randomCharList = random.choices(user_id_list, k=idLength)
    return "".join(randomCharList)

def systemEXIT():
    CommunicateManager().close()
    sys.exit()