from threading import Thread
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


class Wrapper:
    def __init__(self):
        print("Hello")


class Server:
    def __init__(self):
        self.thread = None
        self.server = None

    def start(self):
        self.thread = Thread(target=self.server.serveforever)
        self.server = SimpleWebSocketServer('localhost', 1997, Wrapper)
        self.thread.start()

    def all_connected(self):
        return self.server.connections.values()
