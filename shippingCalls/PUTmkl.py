import requests as rqs
from general.GETerrors import handle
from general.functions import oldHeader

def updateTracking(order, company):
    header = oldHeader(f"{company}Token")
    header["Content-Type"] = "application/json"

    if order["shipName"] == "DX":
        carrier = "DX Delivery"
    elif order["shipName"] == "Parcel force":
        carrier = "Royal Mail"
    else:
        carrier = "Other"

    paramsTrack = {
        "carrier_name":carrier,
        "tracking_number":order["tracking_number"]
    }

    urlTrack = f"https://marketplace.kingfisher.com/api/orders/{order["orderId"]}/tracking"

    rqs.put(urlTrack, json=paramsTrack, headers=header)

