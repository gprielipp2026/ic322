#from status import Status
#from body import Body
#from header import Header
from .responseline import Responseline
from .version import Version

class Response:
    def __init__(self):
        self.startline = Responseline(Version("HTTP/1.1")) 
        self.headers = []
        self.body = None

    def setStatus(self, status):
        self.startline.setStatus(status)

    def addHeader(self, header):
        self.headers.append(header)

    def setBody(self, body):
        self.body = body

    def hasHeader(self, key):
        return self.getHeader(key) != None

    def getHeader(self, key):
        for header in self.headers:
            if header.matches(key):
                return header
        else:
            return None

    def tobytes(self):
        out = self.startline.tobytes() + "\r\n".encode()
        if len(self.headers) > 0:
            #                               for the final header  v       v for the end of the headers
            out += "\r\n".join([str(x) for x in self.headers]).encode() + ("\r\n"*2).encode()
        else:
            out += "\r\n".encode()

        if self.body != None:
            out += self.body.tobytes() + "\r\n".encode()
        
        else:
            out += "\r\n".encode()

        return out
