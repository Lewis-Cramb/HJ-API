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
    mkl_params = {"start_date":dt.datetime.now()-timedelta(1), "end_date":dt.datetime.now()} #Get all orders from yesterday
    if workingDate == "Monday": #Subtract 3 days from the start if its a monday due to weekend orders (i.e friday-sunday)
        mkl_params["start_date":dt.datetime.now()] = timedelta(3)

    #Call APIs using rqs.get() to get the data
    vs_resp = rqs.get("https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json",headers=vs_headers, params=vs_params) #Get all acknowledged orders from VirtualStock
    mkl_resp = rqs.get("https://your-instance.mirakl.net/api/orders",headers=mkl_headers, params=mkl_params)

    #Finally, filter it and join it all together

    #I need the customer name, customer address, order date, courier details including tracking number, and product - also need to send the name of the seller

    #virtualstock - filter this by date too


    return filtered_data

def getSFProdId(instance_url, product, sf_headers):
    query = f"SELECT Id FROM Product2 WHERE Name = '{product['product_name']}"
    prod_params = {"q":query}
    rqst = rqs.get(f"{instance_url}/services/data/v59.0/query",headers=sf_headers,params=prod_params)
    return rqst.json()["records"][0]["Id"]


def postAPI(orders):

    #Define the sales data platform header here (i.e SalesForce)
    sf_headers = headerGeneration("sfToken")
    sf_headers["Content-Type"] = "application/json" #You are making a POST request (giving data) therefore you need to define what format the given data is in  

    #The POST request also requires parameters
    sf_params = {
        "grant_type":"password",
        "client_id": "",
        "client_secret": "",
        "username":"lewis@haywardjardine.co.uk",
        "password": "",
    }

    #You need to first of all get your access codes
    auth_response = rqs.post("https://login.salesforce.com/services/oauth2/token",params=sf_params)

    access_token = auth_response.json().get("access_token")
    instance_url = auth_response.json().get("instance_url")

    #Next we need to format the JSON to SF's standards and send them to SF by order
    for order in orders:

        prod_id = getSFProdId(instance_url, order, sf_headers)

        payload = {
            "Account Name":order["accName"],
            "Status":"PO recieved",
            "Buyer name":order["custName"],
            "PO Receipt Date":order["orderDate"],
            "email address":order["custEmail"],
            "phone num":order["custPhone"],
            "Ship. agent":order["shipName"],
            "exp. ship date":order["expDate"],
            "Product": prod_id,
        }
        response = rqs.post(f"{instance_url}/services/data/v67.0/sobjects/Order/Id",headers=sf_headers,json=payload)

