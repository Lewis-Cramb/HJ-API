#This file is going to be for reading all of the data
import requests as rqs
from datetime import date as dt
import sys
sys.path.append("../HJ-API")
from functions import oldHeader, startDate
from GETs.GETerrors import handle

def getM(company):
    #Define the commerce platform header here 
    mkl_headers = oldHeader(f"{company}Token")
    mkl_params = {"start_date":startDate(), "end_date":dt.today(), "max":100, "offset":0} #Get all orders since last working day

    #Call API using rqs.get() to get the data
    mkl_resp = rqs.get("https://marketplace.kingfisher.com/api/orders",headers=mkl_headers, params=mkl_params)
    error_resp = handle(mkl_resp) #no need to do anything on success, can't refresh login as its not a token
    if error_resp == "Failure":
        return []
    elif error_resp == "Try again":
        return getM()

    mkl_data = mkl_resp.json()

    #Finally, filter it and join it all together

    filtered_orders = []

    if mkl_data["total_count"] > 0:
        for order in mkl_data["orders"]:
            curr = {}
            curr["orderId"] = order["order_id"]
            curr["accName"] = "B&Q Marketplace"
            curr["custName"] = f"{order["customer"]["firstname"]} {order["customer"]["lastname"]}"
            curr["orderDate"] = order["created_date"][0:order["created_date"].index("T")]
            curr["custEmail"] = "" #Customers do not provide emails
            curr["custPhone"] = "0" + order["customer"]["shipping_address"]["phone"]
            curr["shipName"] = order["shipping_company"]
            curr["expDate"] = order["delivery_date"]["latest"][0:order["delivery_date"]["latest"].index("T")] 
            curr["products"] = {}
            curr["cost"] = order["total_price"]
            curr["custPO"] = order["order_id"]
            curr["shipping_address"] = order["customer"]["shipping_address"]

            for product in order["order_lines"]:
                curr["products"][product["product_title"]] = product["quantity"]

            filtered_orders.append(curr)

        
    return filtered_orders

