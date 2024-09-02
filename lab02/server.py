from socket import *
from threading import *

class Server:
    def __init__(self, name: str, port: int, parser):
        self.name = name
        self.port = port
        self.parser = parser
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.start()

    # connect to the socket and start listening
    def start(self):
        print("Server started...")
        self.socket.bind((self.name, self.port))
        print(f"Server bound to {(self.name, self.port)}")
        self.socket.listen(5)
        print("Server listening")
        while True:
            clientSD, addr = self.socket.accept()
            print("Client accepted")
            Thread(target=Server.serve, args=[self.parser, clientSD]).start()

    # implementation part :)
    @staticmethod
    def serve(parser, clientSD):
        print(f'Client({clientSD.fileno()}) connected')
        while True:
            reqStr = clientSD.recv(1024).decode()
            print(f'{reqStr=}\n')
            # client quit :(
            if len(reqStr) == 0:
                print(f'Client({clientSD.fileno()}) disconnected')
                clientSD.close()
                break

            request = parser.requestFrom(reqStr)
            print(f'Client({clientSD.fileno()}):\n{str(request)}')
            response = parser.genResponse(request)
            print("Server:\n" + str(response))

            clientSD.sendall(str(response).encode())
        

