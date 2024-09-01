from httpparser import * 

reqStr = "GET /test/index.html HTTP/1.1\r\nUser-Agent: python\r\n\r\nbody data goes here\r\n"

parser = HttpParser()
print(parser.requestFrom(reqStr))
print(parser.requestFrom("GET /test HTTP/1.1\r\n\r\n\r\n"))
