#this file is used to post orders to xero for invoices
import requests as rqs
import base64

def postToken():
    clientID = open("txts/xrConsID.txt","r").read().strip()
    clientSec = open("txts/xrConsSec.txt","r").read().strip()

    header = {"Authorization" : "Basic " + base64.b64encode(f"{clientID}:{clientSec}"),}
    info = {"grant_type" : "client_credentials", "scope":["accounting.invoices"]}

    token = rqs.post("https://identity.xero.com/connect/token",headers=header,data=info)

    return token.json()["access_token"]


def postData(token, order):
    header = {"Authorization" : f"Bearer {token}"}

    contact = ""
    describe = ""
    quantity = 0

    type = "ACCREC"
    contactID = {"ContactID":contact}
    lineItems = {
        "Description" : describe,
        "Quantity" : quantity,
    }
