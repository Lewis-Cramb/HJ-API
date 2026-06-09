#This file is going to be for reading all of the data
import requests as rqs
from datetime import date as dt
from datetime import timedelta

workingDate = dt.today().strftime("%A")

def oldHeader(filename): #Use this function if you do not need the "bearer" in the auth key (So older APIs without OAuth 2.0)
    with open(f"txts/{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"{token}"}


def printingOrders(orders):
    for order in orders:
        print(f"On {order["orderDate"]}, {order["custName"]} ({order["custPO"]}) ordered:")
        for product in order["products"]:
            print(f"{order["products"][product]}x {product}")
        print(f"For a total of {order["cost"]}")
        print(f"This is to be delivered by {order["shipName"]} by {order["expDate"]}")
        print("\n")

def getAPIs():

    #Define the commerce platform header here (i.e VirtualStock, Mirakl, TrueCommerce)
    mkl_headers = oldHeader("mklToken")


    #All calls will need parameters so you can create a dictionary and add them here
    mkl_params = {"start_date":dt.today()-timedelta(days=1), "end_date":dt.today()} #Get all orders from yesterday
    if workingDate == "Monday": #Subtract 3 days from the start if its a monday due to weekend orders (i.e friday-sunday)
        mkl_params["start_date":dt.today()] = timedelta(days=3)

    #Call APIs using rqs.get() to get the data
    mkl_resp = rqs.get("https://marketplace.kingfisher.com/api/orders",headers=mkl_headers, params=mkl_params)

    mkl_data = mkl_resp.json()
    print(mkl_data)

    #Finally, filter it and join it all together

    #I need site, customer name, order date, customer email, customer phone number, shipping couier name, expected arrival date, products {name:quantity}, cost and customer PO

    filtered_orders = []

    if mkl_data["total_count"] > 0:
        for order in mkl_data["orders"]:
            curr = {}
            curr["accName"] = "[get from sales force]"
            curr["custName"] = order["customer"]["firstname"] + order["customer"]["lastname"]
            curr["orderDate"] = order["created_date"][0:order["created_date"].index("T")]
            curr["custEmail"] = "" #Customers do not provide emails
            curr["shipName"] = order["shipping_company"]
            curr["expDate"] = order["delivery_date"]["latest"][0:order["delivery_date"]["latest"].index("T")] 
            curr["products"] = {}
            curr["cost"] = order["total_price"]
            curr["custPO"] = order["order_id"]

            for product in order["order_lines"]:
                curr["products"][product["product_title"]] = product["quantity"]

            filtered_orders.append(curr)

        
    printingOrders(filtered_orders)


getAPIs()