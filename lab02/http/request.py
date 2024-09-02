from .body import Body
from .header import Header
from .requestline import Requestline

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
    
    def getMethod(self):
        return self.startline.getMethod()

    def getURI(self):
        return self.startline.getURI()

    def hasHeader(self, value):
        return self.getHeader(value) != None

    def getHeader(self, value):
        for header in self.headers:
            if header.matches(value):
                return header
        else:
            return None

    def setBody(self, body):
        self.body = body

    def __str__(self):
        out = str(self.startline) + "\r\n"
        if len(self.headers) > 0:
            out += "\r\n".join([str(x) for x in self.headers]) + "\r\n"
        else:
            out += "\r\n"
        if self.body != None:
            out += str(self.body) + "\r\n"
        else:
            out += "\r\n"
        return out
