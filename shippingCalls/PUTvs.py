import requests as rqs
import json
from datetime import date as dt
from general.functions import vsHeader

def updateTracking(order, line_part_url):
    header = vsHeader()
    header["Content-Type"] = "application/json"
    items = []
    i = 0
    if order["shipName"] == "DX":
        carrier = "DX Freight (Tracked)"
    elif order["shipName"] == "Parcel force":
        carrier = "Royal Mail (Tracked)"
    else:
        carrier = "Kinetics (Untracked)"
    for product in order["products"]:
        part = line_part_url[i][0]
        line = line_part_url[i][1]
        temp = {}
        temp["part_number"] = part
        temp["line_ref"] = line
        temp["quantity"] = order["products"][product]
        temp["supplier_dispatch_date"] = dt.today()
        temp["supplier_delivery_date"] = "" #clarify
        temp["tracking_number"] = order["tracking_number"]
        temp["carrier"] = carrier
        items.append(temp)
        i += 1

    data = json.dump({"items":items})
    rqs.post(f"https://api.sandbox.virtualstock.com/restapi/v4/orders/{line_part_url[0][2]}/dispatch/?format=json", data=data, headers=header)

        