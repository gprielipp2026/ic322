from http.httpparser import HttpParser 
from Server import Server
from http.endpoint import Endpoint
from http.response import Response
from http.body import Body
from http.header import Header
from http.status import Status

def error(msg=""):
    resp = Response()
    resp.setStatus(Status(500))
    resp.setBody(Body(msg))
    return resp

def clean(data):
    # remove all whitespace between items and
    # replace it with SP
    whitespace = "\r"
    output = ""

    for char in data:
        if char in whitespace:
            output += " "
        else:
            output += char

    return output

def filetext(req):
    resp = Response()
    resp.setStatus(Status(200))
    #resp.addHeader(Header("Connection", "close"))

    fn = req.getURI()
    # Load content 
    data = None
    try:
        # this should be customized based on where the server is run
        # perhaps with sys.argv :)
        with open("./files/" + fn, 'r') as fd:
            data = fd.read()
    except Exception as e:
        # error
        return error(e) 

    # figure out Content-Type
    MIME = ""
    if "html" in fn:
        MIME = "text/html"
    elif "js" in fn:
        MIME = "application/javascript" #"text/javascript"
        resp.addHeader(Header("Connection", "close"))
    else:
        return error()

    # set corresponding headers
    resp.addHeader(Header("Content-Type", MIME))
    resp.addHeader(Header("Content-Length", len(data)))
    
    # data to send back
    resp.setBody(Body(data))

    return resp

def unsupported(file):
    resp = Response()

    resp.setStatus(Status(415))

    msg = f'file "{file}" unsupported'

    resp.addHeader(Header("Content-Type", "text/plain"))
    resp.addHeader(Header("Content-Length", len(msg)))

    resp.setBody(Body(msg))

    return resp


def filehandler(req):
    file = req.getURI()

    resp = Response()

    MIMEType = {
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'svg': 'image/svg+xml',
            'ico': 'image/x-icon',
            'html': 'text/html',
            'js': 'text/javascript',
            }

    MIME = ""
    try:
        ending = file[file.find('.')+1:]
        print(f'trying to deal with {ending}')
        MIME = MIMEType[ending]
    except Exception as e:
        return unsupported(file)

    # load file 
    data = None
    try:
        # should open in bniary?
        with open(f'./files/{file}', 'rb') as fd:
            data = fd.read()
    except Exception as e:
        # or try to get it from somewhere else
        print(e)
        return missing(file)

    resp.setStatus(Status(200))
    resp.addHeader(Header("Content-Type", MIME))
    resp.addHeader(Header("Content-Length", len(data)))
    resp.setBody(Body(data))

    return resp

def missing(file):
    resp = Response()
    resp.setStatus(Status(404))
    resp.addHeader(Header("Connection", "close"))

    msg = f'could not find "{file}"'
    resp.addHeader(Header("Content-Type", "text/plain"))
    resp.addHeader(Header("Content-Length", len(msg)))
    resp.setBody(Body(msg))

    return resp

def redirect(req):
    resp = Response()
   
    if len(req.getURI()) > 1:
        return missing(req.getURI())

    resp.setStatus(Status(301))

    resp.addHeader(Header("Location", "/index.html"))
    resp.addHeader(Header("Connection", "close"))

    return resp

"""
This is the actual "server" definition
the above are helper methods that will get called
"""
parser = HttpParser()

# this could/should be a cmdline argument
base = "./files/"
from os import listdir
from os.path import isfile, join
files = [f for f in listdir(base) if isfile(join(base, f))]

print(files)
for fn in files:
    parser.addEndpoint(Endpoint("GET", f'/{fn}', filehandler))

# send / to /index.html
parser.addEndpoint(Endpoint("GET", "/", redirect))

# start the server
server = Server("", 12000, parser)

