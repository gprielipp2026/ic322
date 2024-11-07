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
               }
    headers = load("loginHeaders.txt")
    urlp = "https://login.usna.edu/oam/server/obrareq.cgi?encquery%3DfXBQdQKV%2BxOYnlMtZpxHa%2F1m%2FK6f1PK7QGGfHDmPsDUnpW4iSBciF%2Fn9Ljsecs4Ien3I4miu9ZOHqBkqML0Cz0k1UBak7HU3zWb5qJ6Kdf4ke%2FRDzlqg47JDSbpSlWXhfq8IsC%2B8C48LbpYzF%2FWCKyqhhwW6UFAjqWKoT6%2FGnmWxhl4WKKueVk%2BeeZ7pgSSrcKUPvdv6ls7DWd6mubwOiKfrcgW9jG5F%2BztbUPt4kYcxa%2BlpRlYpVijynSyEW1mOnmJGniW2rKsBX%2B%2F62ogORQ%3D%3D%20agentid%3DUSNA_OHS12c_WebGateAgent%20ver%3D1%20crmethod%3D2"
    resp = session.post(urlp,
                        data=flatten(payload), verify=False)
    print(resp.text)
    #resp = session.post(url, data=flatten(payload), verify=False)
    #print(BeautifulSoup(resp.text, "html.parser"))


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
