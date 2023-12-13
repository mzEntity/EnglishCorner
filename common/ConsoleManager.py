from common.Singleton import singleton

@singleton
class ConsoleManager:
    def __init__(self):
        self.enable = True
    
    
    def print(self, msg):
        if self.enable:
            print(msg)
            
    def enableConsoleManager(self):
        self.enable = True
    
    def disableConsoleManager(self):
        self.enable = False