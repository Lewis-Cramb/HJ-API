import requests as rqs
import sys, urllib.parse
sys.path.append("../hj-api")
from general.functions import getSPToken as getToken
from general.GETerrors import handle

def download(filename="D2C Stock and Sales Sheet.xlsx"):
    token = getToken()
    header = {"Authorization": f"Bearer {token}"}

    enc_filename = urllib.parse.quote(filename)
    driveID = open("txts/spID.txt").read().strip()

    response = rqs.get(f"https://graph.microsoft.com/v1.0/drives/{driveID}/root:/D2C/{enc_filename}:/content", headers=header)

    err = handle(response)
    if err == "Failure":
        return False
    elif err == "Try again":
        return download()

    with open(f"dataPost/{filename}", "wb") as wf:
        wf.write(response.content)
    return True


def upload(filename="D2C Stock and Sales Sheet.xlsx"):
    header = {
        "Authorization": f"Bearer {getToken()}",
        "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    }
    with open(f"dataPost/{filename}", "rb") as rf:
        data = rf.read()

    enc_filename = urllib.parse.quote(filename)
    driveID = open("txts/spID.txt").read().strip()

    response = rqs.put(f"https://graph.microsoft.com/v1.0/drives/{driveID}/root:/D2C/{enc_filename}:/content", headers=header, data=data)

    err = handle(response)
    if err == "Failure":
        return False
    elif err == "Try again":
        return download()
