import random
from common.Config import *

def getRandomUserId():
    idLength = user_id_length
    randomCharList = random.choices(user_id_list, k=idLength)
    return "".join(randomCharList)