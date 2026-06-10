#this file will be for testing the VS sandbox
import requests as rqs
import base64
import json as js

#auth stuff
username = open("txts/vsUsername.txt","r").read().strip()
password = open("txts/vsPassword.txt","r").read().strip()

credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
header = {
    "Authorization": f"Basic {credentials}"
}

#get all orders (may not be used)
response = rqs.get("https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json",headers=header,params={"status":"ORDER"})
json = response.json()
y87 = json["results"][0]
#post an acknowledgement

header['Content-Type'] = "application/json"
items = []
for item in y87["items"]:
    temp = {}
    temp["part_number"] = item["part_number"]
    temp["line_ref"] = item["line_reference"]
    temp["quantity"] = item["quantity"]
    items.append(temp)

info = js.dumps(items)

ackY87 = rqs.post("https://api.sandbox.virtualstock.com/restapi/v4/orders/287fe779-a5fb-4434-8903-4b421510056d/acknowledge/?format=json",headers=header,data=info)