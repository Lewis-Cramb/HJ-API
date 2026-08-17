import requests as rqs, xml.etree.ElementTree as xml
import sys
sys.path.append("../HJ-API")
from general.functions import xeroToken as token, xeroDate as date, findMax

def invoiceNumber():
    header = {"Authorization":f"Bearer {token()}"}
    params = {"where":f"Date>={date()} AND (Status==\"AUTHORISED\" OR Status=\"DRAFT\")"}

    response = rqs.get("https://api.xero.com/api.xro/2.0/Invoices", headers=header, params=params)
    invoiceNumbers = []
    root = xml.fromstring(response.text)
    invoices = root.find("Invoices")
    for invoice in invoices.findall("Invoice"):
        invoiceNumbers.append(invoice.find("InvoiceNumber").text)

    properNumbers = []
    for number in invoiceNumbers:
        if "INV" not in number:
            properNumbers.append(number)

    return findMax(properNumbers)+1
