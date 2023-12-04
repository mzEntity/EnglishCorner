from common.Singleton import singleton

@singleton
class Background:
    def __init__(self):
        pass

    def executeCommand(self, command):
        receipt = command.execute()
        return receipt
        


