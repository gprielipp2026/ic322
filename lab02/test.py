#import sys
#import os
#SCRIPT_DIR=os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.dirname(SCRIPT_DIR))
#sys.path.append(os.path.dirname(SCRIPT_DIR+"/http"))

from http.httpparser import HttpParser 
from server import Server
from http.endpoint import Endpoint
from http.response import Response
from http.body import Body
from http.header import Header
from http.status import Status

def echo(req):
    target = req.getURI()
    val = target[6:]

    resp = Response()
    resp.setStatus(Status(200))

    resp.addHeader(Header("Content-length", len(val)))

    resp.setBody(Body(val))

    return resp

def ok(req):
    resp = Response()
    resp.setStatus(Status(200))
    resp.addHeader(Header("Connection", "close"))

    return resp

parser = HttpParser()

parser.addEndpoint(Endpoint("GET", "/echo", echo))
parser.addEndpoint(Endpoint("GET", "/", ok))

server = Server("", 9999, parser)

