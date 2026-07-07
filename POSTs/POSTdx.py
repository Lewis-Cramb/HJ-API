#this file will be used to create an order on dx and return the tracking number
import requests as rqs, base64 as b64, xml.etree.ElementTree as xml
from datetime import datetime as dt
from Lists.dxPlatform import HJ, DT
from Lists.weights import weight


def tracking(product,order):
    
    if product in HJ:
        details = {
            "DXAccountNumber": open("txts/dxHjAccount.txt").read().strip(),
            "OrigServiceCentre":"70",
            "Password":open("txts/dxHjPassword.txt").read().strip()
        }
    elif product in DT:
        details = {
            "DXAccountNumber": open("txts/dxDtAccount.txt").read().strip(),
            "OrigServiceCentre":"70",
            "Password":open("txts/dxDtPassword.txt").read().strip()
        }


    token = rqs.post(f"https://itd.dx-track.com/DespatchManager.API.Service.DM6Lite_Test/DM6LiteService.svc/GetSessionKey", json=details)
    xmlNamespace = {"ns": "http://schemas.datacontract.org/2004/07/DespatchManager.API.Service.DM6Lite.Responses"}

    session_key = xml.fromstring(token.text).findtext("ns:SessionKey",namespaces=xmlNamespace)
    authHead = f"<AuthHeader><SessionKey>{session_key}</SessionKey></AuthHeader>"

    headers = {
        "AuthHeader": authHead,
        "Context-type": "text/xml charset=utf-8"
    }

    manifest_date = int(dt.now().timestamp() * 1000)

    contents = []
    for product in order["products"].keys():
        contents.append(
            {
                "ContentDescriptionID": 1,
                "ContentDescription": "CartonKG",
                "ContentQuantity": order["products"][product], #fill this in
                "ContentTotalWeight": weight[product]*order["products"][product] #fill this in
            }
        )

    payload = {
        "DXAccountNumber": f"{details["DXAccountNumber"]}",
        "OrigServiceCentre": "70",
        "ManifestDate": f"/Date({manifest_date}+0000)/",
        "ConsignmentReference1": "", #fill this in 
        "ServiceCode": "2D",  
        "DeliveryName": order["customer_name"],
        "DeliveryAddress1": order["address_1"],
        "DeliveryAddress2": order["address_2"],
        "DeliveryPostcode": order["post_code"],
        "DeliveryPhoneNumber": order["customer_phone"],
        "DeliveryContact": order["customer_name"],
        "Contents": contents
    }
