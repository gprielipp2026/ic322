from .request import Request
from .body import Body
from .header import Header
from .requestline import Requestline 
from .status import Status
from .response import Response

class HttpParser:
    def __init__(self):
        self.state = 0 
        self.endpoints = []

    def requestline(self, reqLine, request):
        """
        start-line = Request-Line | Status-Line
        #note: should be a request line in this method
        
        Request-Line = Method SP Request-URI SP HTTP-Version CRLF
        """
        
        reqObjs = reqLine[0].split(" ")
        method = reqObjs[0]
        target = reqObjs[1]
        version = reqObjs[2]

        request.setStartline(Requestline(method, target, version))

        self.state += 1 


    def headers(self, reqLine, request):
        """
        message-header = field-name ":" [ field-value  ]
        field-name     = token
        field-value    = *( field-content | LWS  )
        field-content  = <the OCTETs making up the field-value
                         and consisting of either *TEXT or combinations
                         of token, separators, and quoted-string>
        """

        for reqObj in reqLine[1:]:
            # no more headers to read
            if reqObj == '':
                break
            name, value = (reqObj[:reqObj.find(":")], reqObj[reqObj.find(':')+1:])
            request.addHeader(Header(name, value))

        self.state += 1


    def body(self, reqLine, request):
        """
        message-body = entity-body | <entity-body encoded as per Transfer-Encoding>
        """

        request.setBody(Body(reqLine[-1]))
        
        self.state += 1

    """
    generates an object representing HTTP Request
    """
    def requestFrom(self, reqstr):
        """
        Message format:
            start-line
            *(message-header CRLF)
            CRLF
            [ message-body ]

        start-line = Request-Line | Status-Line
        # note: should be a request line in this method
        """

        request = Request()


        """
        states:
            0 - read start line
            1 - read all message-headers
            2 - read message-body
            3 - done
        """
        self.state = 0
        funcs = [self.requestline, self.headers, self.body]

        reqLines = reqstr.split("\r\n")[:-1]

        while self.state != 3:
            funcs[self.state](reqLines, request) 

        return request


    """
    generates a response for the server to send
    """
    def genResponse(self, request):
        for endpoint in self.endpoints:
            if endpoint.match(request.getMethod(), request.getURI()):
                return endpoint.handleRequest(request)
        else:
            # 404 Not Found
            resp = Response()
            resp.setStatus(Status(404))
            return resp

    def addEndpoint(self, endpoint):
        self.endpoints.append(endpoint)
