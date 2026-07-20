#this file is used to post orders to xero for invoices
import requests as rqs
from base64 import b64encode as b64
import xml.etree.ElementTree as ET
import sys
sys.path.append("../HJ-API")
from functions import convertNames as conversion, format_date as formatting, xeroDue as dd

def postToken():
    clientID = open("txts/xeroID.txt","r").read().strip()
    clientSec = open("txts/xeroSec.txt","r").read().strip()

    header = {"Authorization" : "Basic " + b64(f"{clientID}:{clientSec}".encode()).decode()}
    info = {"grant_type" : "client_credentials", "scope":"accounting.invoices accounting.settings"}

    token = rqs.post("https://identity.xero.com/connect/token",headers=header,data=info)
    temp = token.json()
    print()
    return token.json()["access_token"]


def postData(order, source):
    header = {"Authorization" : f"Bearer {postToken()}"}
    if source == "JLP":
        custName = "JLEWIS02"
    elif "B&Q" in source:
        custName = "B&Q001"

    lineItems = []
    for product in order["products"].keys():
        lineItems.append(
            {
                "ItemCode":product,
                "quantity":order["products"][product]
            }
        )


    invoice = {
        "Invoices": [{
            "Type": "ACCREC",
            "Contact":{
                "Name":custName
            },
            "Reference":order["custPO"],
            "DueDate":dd(),
            "LineItems":lineItems,
            "BrandingThemeID": "ff5cbad5-f371-4fd2-a13d-e8ac5e719946",
        }
        ]
    }

    response = rqs.post("https://api.xero.com/api.xro/2.0/Invoices", headers=header, json=invoice)
    