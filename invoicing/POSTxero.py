#this file is used to post orders to xero for invoices
import requests as rqs
from base64 import b64encode as b64
import xml.etree.ElementTree as ET
from general.functions import xeroDue as dd
from invoicing.GETxero import invoiceNumber as invNum

def postToken():
    clientID = open("txts/xeroID.txt","r").read().strip()
    clientSec = open("txts/xeroSec.txt","r").read().strip()

    header = {"Authorization" : "Basic " + b64(f"{clientID}:{clientSec}".encode()).decode()}
    info = {"grant_type" : "client_credentials", "scope":"accounting.invoices accounting.settings"}

    token = rqs.post("https://identity.xero.com/connect/token",headers=header,data=info)    
    return token.json()["access_token"]


def postData(order):
    header = {"Authorization" : f"Bearer {postToken()}"}
    custName = "John Lewis Partnership GBP"

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
            "Reference":order["reference"],
            "DueDate":dd(),
            "InvoiceNumber":invNum(),
            "LineItems":lineItems,
            "BrandingThemeID": "ff5cbad5-f371-4fd2-a13d-e8ac5e719946",
        }
        ]
    }

    response = rqs.post("https://api.xero.com/api.xro/2.0/Invoices", headers=header, json=invoice)
    