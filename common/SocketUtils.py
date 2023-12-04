import socket
from common.Singleton import singleton

@singleton
class SocketManager:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def recv(self, byteCount=1024):
        return self.sock.recvfrom(byteCount)

    def bind(self, addr):
        return self.sock.bind(addr)

    def sendTo(self, packetBytes, addr):
        return self.sock.sendto(packetBytes, addr)

    def close(self):
        self.sock.close()