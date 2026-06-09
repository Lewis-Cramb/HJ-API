#This file is going to be for reading all of the data
import requests as rqs
import datetime as dt
from datetime import timedelta

workingDate = dt.datetime.now().strftime("%A")

def headerGeneration(filename): #This function generates the headers needed for the JWT (JSON Web Token)
    with open(f"{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"Bearer {token}"}

def oldHeader(filename): #Use this function if you do not need the "bearer" in the auth key (So older APIs without OAuth 2.0)
    with open(f"{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"{token}"}


def getAPIs():

    #Define the commerce platform header here (i.e VirtualStock, Mirakl, TrueCommerce)
    vs_headers = headerGeneration("vsToken")
    mkl_headers = oldHeader("mklToken")


    #All calls will need parameters so you can create a dictionary and add them here
    vs_params = {"status":"ORDER_ACK"}
    mkl_params = {"start_date":dt.datetime.now()-timedelta(1), "end_date":dt.datetime.now(), "order_state_codes":"STAGING"} #Get all orders from yesterday
    if workingDate == "Monday": #Subtract 3 days from the start if its a monday due to weekend orders (i.e friday-sunday)
        mkl_params["start_date":dt.datetime.now()] = timedelta(3)

    #Call APIs using rqs.get() to get the data
    vs_resp = rqs.get("https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json",headers=vs_headers, params=vs_params) #Get all acknowledged orders from VirtualStock
    mkl_resp = rqs.get("https://your-instance.mirakl.net/api/orders",headers=mkl_headers, params=mkl_params)

    vs_data = vs_resp.json()
    mkl_data = mkl_resp.json()

    #Finally, filter it and join it all together

    #I need site, customer name, order date, customer email, customer phone number, shipping couier name, expected arrival date, products {name:quantity}, cost and customer PO

    #virtualstock - filter this by date too

    filtered_orders = []

    if vs_data["results"] != []:
        for order in vs_data["results"]: #add phone number
            curr = {}
            curr["accName"] = "John Lewis D2C"
            curr["custName"] = order["shipping_address"]["full_name"]
            curr["orderDate"] = order["order_date"][0:order["order_date"].index("T")]
            curr["custEmail"] = order["shipping_address"]["email"]
            curr["shipName"] = "TO GET"
            curr["expDate"] = order["items"]["promised_date"][0:order["items"]["promised_date"].index("T")]
            curr["products"] = {}
            curr["cost"] = order["total"]
            curr["custPO"] = order["end_user_purchase_order_reference"]

            for product in curr["items"]:
                curr["products"][product["name"]] = product["quantity"]

            filtered_orders.append(curr)

    if mkl_data["total_count"] > 0:
        for order in mkl_data["orders"]:
            curr = {}
            curr["accName"] = "[get from sales force]"
            curr["custName"] = order["customer"]["firstname"] + order["customer"]["lastname"]
            curr["orderDate"] = order["created_date"][0:order["created_date"].index("T")]
            curr["custEmail"] = order["customer"]["email"]
            curr["shipName"] = order["shipping_company"]
            curr["expDate"] = order["delivery_date"]["latest"][0:order["delivery_date"]["latest"].index("T")] #Check this one out - is it the latest date they use for mirakl?
            curr["products"] = {}
            curr["cost"] = order["total_price"]
            curr["custPO"] = order["end_user_purchase_order_reference"]

            for product in order["order_lines"]:
                curr["products"][product["product_title"]] = product["quantity"]

            filtered_orders.append(curr)

        
    return filtered_orders

