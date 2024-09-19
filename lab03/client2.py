#!/usr/bin/env python3

from requests import *
from bs4 import BeautifulSoup
import json
import getpass
import random

def load(fn):
    ret = {}
    with open(fn, 'r') as fd:
        for line in fd.readlines():
            line = line.strip()
            if line != "":
                key, value = line.split(":", 1)
                ret[key.strip()] = value.strip()

    return ret

def flatten(data:dict, sep:str ='&') -> str:
    return sep.join([f'{key}={value}' for key,value in data.items()])

def login(session):
    uname = input("Username: ")
    pword = getpass.getpass(prompt="Password: ")

    url = "https://login.usna.edu/oam/server/auth_cred_submit"
    payload = {
                "username": uname, 
                "password": pword, 
                "request_id": str( random.getrandbits(64) ),
                "displayLangSelection": "false",
                "Languages": ""
               }
    headers = load("loginHeaders.txt")
    resp = session.get("https://login.usna.edu/oam/server/obrareq.cgi",  verify=False)
    print(resp.text)
    resp = session.post(url, data=flatten(payload), verify=False)
    print(BeautifulSoup(resp.text, "html.parser"))


def getInfo() -> dict:
    isDone = input("Are you done [y/N]? ") or "N"
    if isDone == 'y':
        return {"done": True}
    alpha = input("Alpha: ")
    lname = input("Last Name: ")
    comp  = input("Company: ")
    acyr  = input("Ac Yr Ending: ") or "2025" # could programatically determine
    sem   = input("Semester: ") or "FALL"
    block = input("Blk Nbr: ") or "1"
    major = input("Major Code: ") 
    advis = input("Adviser (First+Last): ")

    return {
            "P_ALPHA": alpha,
            "P_LAST_NAME": lname,
            "P_MICO_CO_NBR": comp,
            "P_SECOF_COOF_SEBLDA_AC_YR": acyr,
            "P_SECOF_COOF_SEBLDA_SEM": sem,
            "P_SECOF_COOF_SEBLDA_BLK_NBR": block,
            "P_MAJOR_CODE": major,
            "P_NOMI_FORMATTED_NAME": advis,
            "Z_ACTION": "QUERY",
            "Z_CHK": "0",
            "done": False
            }

def parseResponse(response):
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.body)


#reqheaders = load("requestHeaders.txt")

session = Session()
login(session)
print()

url = "https://mids.usna.edu/ITSD/mids/drgwq010$mids.actionquery"

while True:
    request = getInfo()
    if request['done']:
        break
    del request['done']
    
    print(session.cookies)
    
    resp = session.post(url, data=flatten(request))
    parseResponse(resp)

session.close()
