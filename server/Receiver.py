from common.Singleton import singleton


@singleton
class Receiver:
    def __init__(self):
        pass

    def action(self, cmdStr):
        return f"Receiver get command {cmdStr}"