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


