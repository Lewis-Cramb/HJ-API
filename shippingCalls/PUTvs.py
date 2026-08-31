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
        carrier = "dx-untracked"
    elif order["shipName"] == "Parcel force":
        carrier = "royal-mail-untracked"
    else:
        carrier = "kinetics-untracked"
    for product in order["products"]:
        part = line_part_url[i][0]
        line = line_part_url[i][1]
        temp = {}
        temp["part_number"] = part
        temp["line_ref"] = line
        temp["quantity"] = order["products"][product]
        temp["supplier_dispatch_date"] = dt.today().strftime("%Y-%m-%d")
        temp["supplier_delivery_date"] = order["promised_date"]
        temp["tracking_number"] = order["tracking_number"]
        temp["carrier"] = carrier
        items.append(temp)
        i += 1

    data = json.dumps({"items":items})
    url = f"https://api.virtualstock.com/restapi/v4/orders/{line_part_url[0][2]}/dispatch/?format=json"
    response = rqs.post(url, json=data, headers=header)
        