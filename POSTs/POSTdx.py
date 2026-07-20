#this file will be used to create an order on dx and return the tracking number
import requests as rqs, base64 as b64, xml.etree.ElementTree as xml
from datetime import datetime as dt
from Lists.dxPlatform import HJ, DT
from Lists.weights import weight
from GETs.GETerrors import handle

def payload(product,order, contents):

    contents.append({
        "ContentDescriptionID": 1,
        "ContentDescription": "CartonKG",
        "ContentQuantity": order["products"][product],
        "ContentTotalWeight": weight[product]*order["products"][product]
    })


def tracking(product,order, contents):
    
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


    token = rqs.post(f"https://dm6api.dxfreight.co.uk/DespatchManager.API.Service.DM6Lite/DM6LiteService.svc/GetSessionKey", json=details)
    xmlNamespace = {"ns": "http://schemas.datacontract.org/2004/07/DespatchManager.API.Service.DM6Lite.Responses"}
    session_key = xml.fromstring(token.text).findtext("ns:SessionKey",namespaces=xmlNamespace)
    authHead = f"<AuthHeader><SessionKey>{session_key}</SessionKey></AuthHeader>"

    headers = {
        "AuthHeader": authHead,
        "Context-type": "text/xml charset=utf-8"
    }

    manifest_date = int(dt.now().timestamp() * 1000)

    if len(order["custPO"]) > 10:
        order["custPO"] = order["custPO"][0:10]

    payload = {
        "DXAccountNumber": f"{details["DXAccountNumber"]}",
        "OrigServiceCentre": "70",
        "ManifestDate": f"/Date({manifest_date}+0000)/",
        "ConsignmentReference1": order["custPO"], 
        "ServiceCode": "3D",  #no option for 2 day delivery
        "DeliveryName": order["shipping_address"]["customer_name"],
        "DeliveryAddress1": order["shipping_address"]["address_1"],
        "DeliveryAddress2": order["shipping_address"]["address_2"],
        "DeliveryPostcode": order["shipping_address"]["post_code"],
        "DeliveryPhoneNumber": order["shipping_address"]["customer_phone"],
        "DeliveryContact": order["shipping_address"]["customer_name"],
        "Contents": contents
    }

    response = rqs.post("https://dm6api.dxfreight.co.uk/DespatchManager.API.Service.DM6Lite/DM6LiteService.svc/AddConsignment", json=payload, headers=headers)
    error_resp = handle(response)
    if error_resp == "Failure":
        return []
    elif error_resp == "Try again":
        return tracking(product, order, contents)

    namespace = {"ns": "http://schemas.datacontract.org/2004/07/DespatchManager.API.Service.DM6Lite.Responses"}
    root = xml.fromstring(response.text)
    trackNums = root.find("ns:TrackingNumbers", namespaces=namespace)
    consRes = trackNums.find("ns:AddConsignmentResponse.TrackingNumbersInfo", namespaces=namespace)
    trackNum = consRes.findtext("ns:TrackingNumber", namespaces=namespace)
    return trackNum


