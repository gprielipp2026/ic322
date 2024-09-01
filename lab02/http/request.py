from body import Body
from header import Header
from startline import Startline

class Request:
    def __init__(self):
        self.startline = None
        self.headers = [] 
        self.body = None

    def setStartline(self, startline):
        self.startline = startline

    def addHeader(self, header):
        #self.headers[header.getName()] = header.getValue()
        self.headers.append(header)

    def setBody(self, body):
        self.body = body

    def __str__(self):
        return str(self.startline) + "\r\n" + "\r\n".join([str(x) for x in self.headers]) + "\r\n" + str(self.body) + "\r\n"
