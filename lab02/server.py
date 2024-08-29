from socket import *
from threading import *

class Server:
    def __init__(self, name: str, port: int, parser):
        self.name = name
        self.port = port
        self.parser = parser
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.start()

    # connect to the socket and start listening
    def start(self):
        self.socket.bind((self.name, self.port))
        self.socket.listen(1)
        while True:
            clientSD, addr = self.socket.accept()
            Thread(target=Server.serve, args=[parser, clientSD])

    # implementation part :)
    @staticmethod
    def serve(parser, clientSD):
        while True:
            reqStr = clientSD.recv(4096).decode()
            # client quit :(
            if len(reqStr) == 0:
                clientSD.close()
                break

            request = parser.requestFrom(reqStr)
            response = parser.genResponse(request)

            clientSD.sendall(str(response).encode())
        

