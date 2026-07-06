import requests as rqs
import xml.etree.ElementTree as ET
import base64
from datetime import datetime

# getSessionKey

details = {
    "DXAccountNumber": open("txts/dxAccount.txt").read().strip(),
    "OrigServiceCentre":"70",
    "Password":open("txts/dxPassword.txt").read().strip()
}

tokenResponse = rqs.post(f"https://itd.dx-track.com/DespatchManager.API.Service.DM6Lite_Test/DM6LiteService.svc/GetSessionKey", json=details)

root = ET.fromstring(tokenResponse.text)
namespace = {"ns": "http://schemas.datacontract.org/2004/07/DespatchManager.API.Service.DM6Lite.Responses"}

session_key = root.findtext("ns:SessionKey",namespaces=namespace)


authHead = f"<AuthHeader><SessionKey>{session_key}</SessionKey></AuthHeader>"

headers = {
    "AuthHeader": authHead,
    "Context-type": "text/xml charset=utf-8"
}

# getConsignemntNumbers
consignmentNumbers = []

# Convert date to Unix timestamp (milliseconds)
manifest_date = int(datetime.now().timestamp() * 1000)

payload = {
    "DXAccountNumber": "93018638",
    "OrigServiceCentre": "70",
    "ManifestDate": f"/Date({manifest_date}+0000)/",
    "ConsignmentReference1": "ORDER-12345", 
    "ServiceCode": "ON",  
    "DeliveryName": "John Doe",
    "DeliveryAddress1": "123 Main Street",
    "DeliveryAddress2": "Fake place",
    "DeliveryPostcode": "G52 4XX",
    "DeliveryPhoneNumber": "07000000000",
    "DeliveryContact": "John",
    "Contents": [
        {
            "ContentDescriptionID": 1,  # CartonKG
            "ContentDescription": "CartonKG",
            "ContentQuantity": 1,
            "ContentTotalWeight": 5
        }
    ]
}

response = rqs.post("https://itd.dx-track.com/DespatchManager.API.Service.DM6Lite_Test/DM6LiteService.svc/AddConsignment", json=payload, headers=headers)

print(response.text)


root = ET.fromstring(response.text)
consignmentNumbers.append(root.findtext("ns:ConsignmentNumber", namespaces=namespace))



# Convert date to Unix timestamp (milliseconds)
manifest_date = int(datetime.now().timestamp() * 1000)

payload = {
    "DXAccountNumber": "93018638",
    "OrigServiceCentre": "70",
    "ManifestDate": f"/Date({manifest_date}+0000)/",
    "ConsignmentReference1": "ORDER-67890", 
    "ServiceCode": "ON",  
    "DeliveryName": "Jane Doe",
    "DeliveryAddress1": "123 Main Street",
    "DeliveryAddress2": "Fake place",
    "DeliveryPostcode": "G12 8QQ",
    "DeliveryPhoneNumber": "07111111111",
    "DeliveryContact": "Jane",
    "Contents": [
        {
            "ContentDescriptionID": 1,  # CartonKG
            "ContentDescription": "CartonKG",
            "ContentQuantity": 2,
            "ContentTotalWeight": 10
        }
    ]
}

response = rqs.post("https://itd.dx-track.com/DespatchManager.API.Service.DM6Lite_Test/DM6LiteService.svc/AddConsignment", json=payload, headers=headers)

root = ET.fromstring(response.text)
consignmentNumbers.append(root.findtext("ns:ConsignmentNumber", namespaces=namespace))



print(consignmentNumbers)
# getLabels

for number in consignmentNumbers:
    payload = {
        "ConsignmentNumber": number,
        "LabelReturnType": 0,  # 0=PDF, 1=ZPL, 2=Datamax
        "PrintSelection": 0,   # 0=unprinted labels
        "RoutingStream": "F",
        "PDFLabelConfig": {
            "labelSetup": 1,      # 1 label per page
            "startingPosition": 1
        }
    }

    labelResponse = rqs.post("https://itd.dx-track.com/DespatchManager.API.Service.DM6Lite_Test/DM6LiteService.svc/GetLabels", json=payload, headers=headers)

    print(labelResponse.text)

    label_data = ET.fromstring(labelResponse.text).findtext("ns:label",namespaces=namespace)

    pdf_bytes = base64.b64decode(label_data)
    with open(f"DX-Sandbox/label-{number}.pdf", "wb") as f:
        f.write(pdf_bytes)
