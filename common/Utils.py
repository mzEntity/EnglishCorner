import random
from common.Config import *
import sys
from common.SocketUtils import CommunicateManager

def getRandomUserId():
    idLength = user_id_length
    return generateRandomStr(idLength)

def generateRandomStr(count):
    return "".join(random.choices(random_list, k=count))

def systemEXIT():
    CommunicateManager().close()
    sys.exit()
    