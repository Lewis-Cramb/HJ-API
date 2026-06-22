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

def posting(order):
    orderURL = order["url"]
    orderURL = orderURL[orderURL.index("orders/")+7:-1]

    header['Content-Type'] = "application/json"
    items = []
    for item in order["items"]:
        temp = {}
        temp["part_number"] = item["part_number"]
        temp["line_ref"] = item["line_reference"]
        temp["quantity"] = item["quantity"]
        temp["supplier_delivery_date"] = item["promised_date"]
        temp["fulfillment_route"] = "Direct to Customer"
        items.append(temp)

    
    if order["status"] == "ORDER":
        acknowledge(orderURL, header, items)
    elif order["status"] == "ORDER_ACK":
        dispatch(orderURL, header, items)

def acknowledge(orderURL, header, items):
    for item in items:
        item["fulfillment_route"] = "Direct to customer"
    info = js.dumps({"items": items})
    acknowledgement = rqs.post(f"https://api.sandbox.virtualstock.com/restapi/v4/orders/{orderURL}/acknowledge/?format=json",headers=header,data=info)
    print(acknowledgement.text)


def dispatch(orderURL, header, items):
    for i,item in enumerate(items):
        item["supplier_delivery_date"] = item["supplier_delivery_date"][:item["supplier_delivery_date"].index("T")]
        item["supplier_dispatch_date"] = item["supplier_delivery_date"]
        item["carrier"] = "dpd"
        item["tracking_number"] = 12345+i
    info = js.dumps({"items": items})
    dispatched = rqs.post(f"https://api.sandbox.virtualstock.com/restapi/v4/orders/{orderURL}/dispatch/?format=json",headers=header,data=info)
    print(dispatched.text)


#get all orders (may not be used)
response = rqs.get("https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json",headers=header)
json = response.json()
for order in json["results"]:
    posting(order)

