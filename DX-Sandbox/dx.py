import requests as rqs
import xml.etree.ElementTree as ET

details = {
    "DXAccountNumber": open("txts/dxAccount.txt").read().strip(),
    "OrigServiceCentre":"70",
    "Password":open("txts/dxPassword.txt").read().strip()
}

tokenResponse = rqs.post(f"https://itd.dx-track.com/DespatchManager.API.Service.DM6Lite_Test/DM6LiteService.svc/GetSessionKey", json=details)

print(f"Response Text: {tokenResponse.text}")

root = ET.fromstring(tokenResponse.text)
namespace = {"ns": "http://schemas.datacontract.org/2004/07/DespatchManager.API.Service.DM6Lite.Responses"}

session_key = root.findtext("ns:SessionKey",namespaces=namespace)


authHead = f"<AuthHeader><SessionKey>{session_key}</SessionKey></AuthHeader>"

headers = {
    "AuthHeader": authHead,
    "Context-type": "text/xml charset=utf-8"
}

consignmentNumbers = ["L3014499","L3049429"]

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

    import base64
    pdf_bytes = base64.b64decode(label_data)
    with open(f"label-{number}.pdf", "wb") as f:
        f.write(pdf_bytes)
