#This file is for the posting of the data to salesforce
import requests as rqs
from datetime import datetime
from functions import format_date


def getSFProdId(instance_url, product, sf_headers):
    query = f"SELECT Id, Pricebook2Id FROM PricebookEntry WHERE Product2.Name = '{product}' AND IsActive = true"
    prod_params = {"q":query}
    rqst = rqs.get(f"{instance_url}/services/data/v67.0/query",headers=sf_headers,params=prod_params)
    print(rqst.json())
    return rqst.json()["records"][0]["Id"], rqst.json()["records"][0]["Pricebook2Id"]

def getSFAccName(instance_url, account, sf_headers):
    query = f"SELECT Id from Account WHERE Name = '{account}'"
    acc_params = {"q":query}
    rqst = rqs.get(f"{instance_url}/services/data/v67.0/query", headers=sf_headers, params=acc_params)
    return rqst.json()["records"][0]["Id"]


def postAPI(orders):

    #The POST request needs to be authenticated

    sf_auth_params = {
        "grant_type":"client_credentials",
        "client_id": open("txts/sfConsID.txt","r").read(),
        "client_secret": open("txts/sfConsSec.txt","r").read(),
    }

    #You need to first of all get your access codes
    auth_response = rqs.post("https://haywardjardine.my.salesforce.com/services/oauth2/token",params=sf_auth_params)

    access_token = auth_response.json().get("access_token")
    instance_url = auth_response.json().get("instance_url")

    print(access_token)
    print(instance_url)

    print(auth_response.json())
    print()

    #Define the sales data platform header here (i.e SalesForce)
    sf_headers = {"Authorization": f"Bearer {access_token}"}
    sf_headers["Content-Type"] = "application/json" #You are making a POST request (giving data) therefore you need to define what format the given data is in  

    #Next we need to format the JSON to SF's standards and send them to SF by order

    for order in orders:
        placeholderOrder = list(order["products"].keys())[0]
        _,pricebookID = getSFProdId(instance_url, placeholderOrder, sf_headers) 

        payload = {
            "AccountId":getSFAccName(instance_url, order["accName"], sf_headers),
            "Status":"PO received",
            "Buyer_name__c":order["custName"],
            "EffectiveDate":format_date(order["orderDate"]),
            "email_address__c":order["custEmail"],
            "phone_num__c":order["custPhone"],
            "Ship_agent__c":order["shipName"],
            "exp_ship_date__c":format_date(order["orderDate"]),
            "Type":"D2C",
            "Cust_PO__c":order["custPO"],
            "Shipping_port__c":"Collection",
            "courier_tracking_info__c":"WORKING ON",
            "Pricebook2Id":pricebookID,
            "CurrencyIsoCode":"GBP",
        }
        response = rqs.post(f"{instance_url}/services/data/v67.0/sobjects/Order/Id",headers=sf_headers,json=payload)
        print("Order created")
        print(response.json())
        print()

        for key in order["products"]:
            #lastly we need to link the product to the order

            prod_id,_ = getSFProdId(instance_url,key, sf_headers)
            
            product_payload = {
                "OrderID": response.json().get("id"),
                "PricebookEntryID":prod_id,
                "Quantity":order["products"][key],
                "UnitPrice":order["cost"],
            }

            prod_response = rqs.post(f"{instance_url}/services/data/v67.0/sobjects/OrderItem/Id",headers=sf_headers,json=product_payload)
            print(prod_response.json())
            print(f"{key} added")

#Needed format for the orders variable
#
#orders = [{"accName": "John Lewis D2C", 
# "custName": "Lewis Cramb", "orderDate":"08/06/2026", 
# "custEmail":"test@test.test", "custPhone":"0000000000", 
# "shipName":"DX", "expDate":"08/06/2026", 
# "products":{"Buffalo 5 Shelf Metal Cabinet":1},
# "cost":"450", "custPO":"000000000011111111111"}]
