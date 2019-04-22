from threading import Thread
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


class Wrapper(WebSocket):
    # def __init__(self):
        # print("Hello")
    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')


class Server:
    def __init__(self):
        self.thread = None
        self.server = None

    def start(self):
        self.server = SimpleWebSocketServer('localhost', 1997, Wrapper)
        self.thread = Thread(target=self.server.serveforever)
        self.thread.start()

    def all_connected(self):
        return self.server.connections.values()
