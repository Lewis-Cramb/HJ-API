#This file is going to be for reading all of the data
import requests as rqs
from datetime import date as dt
from functions import vsHeader, startDate
from GETerrors import handle


def getVS():
    #Create the additional information for the request
    vs_headers = vsHeader()
    vs_params = {"status":"ORDER_ACK"}

    #Call APIs using rqs.get() to get the data
    vs_resp = rqs.get("https://api.virtualstock.com/restapi/v4/orders",headers=vs_headers, params=vs_params) #Get all acknowledged orders from VirtualStock
    error_resp = handle(vs_resp) #no need to do anything on success, can't refresh login as its not a token
    if error_resp == "Failure":
        return []
    elif error_resp == "Try again":
        return getVS()


    vs_data = vs_resp.json()

    #Finally, filter it and join it all together
    filtered_orders = []

    for order in vs_data["results"]: #add phone number
        if dt.fromisoformat(order["order_date"][0:order["order_date"].index("T")]) < startDate(): 
            curr = {}
            price = 0.0
            curr["accName"] = "John Lewis D2C"
            curr["custName"] = order["shipping_address"]["full_name"]
            curr["orderDate"] = order["order_date"][0:order["order_date"].index("T")]
            curr["custEmail"] = order["shipping_address"]["email"]
            curr["custPhone"] = order["shipping_address"]["phone"]
            curr["shipName"] = "TO GET"
            curr["expDate"] = order["items"][0]["promised_date"][:order["items"][0]["promised_date"].index("T")]
            curr["products"] = {}#
            for item in order["items"]:
                price += float(item["subtotal"])
            curr["cost"] = f"{price}"
            curr["custPO"] = order["end_user_purchase_order_reference"]

            for product in curr["items"]:
                curr["products"][product["name"]] = product["quantity"]

            filtered_orders.append(curr)

        
    return filtered_orders