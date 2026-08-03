import requests as rqs
import sys
from datetime import datetime as dt, timedelta as td
sys.path.append("../HJ-API/")
from dataPOST.POSTsf import getAuthToken as sfAuth


def pullSF():
    access_token,instance_url = sfAuth()

    today = dt.today().date()
    monday = today - td(days=today.weekday()+1) 
    last_monday = monday - td(days=7)   

    print(monday)
    print(last_monday)

    query = f"SELECT Id, OrderNumber, Account.Name, (SELECT Id, Product2.Name, Quantity FROM OrderItems) FROM order WHERE CreatedDate >= {last_monday}T00:00:00Z AND CreatedDate <= {monday}T00:00:00Z ORDER BY CreatedDate DESC"

    param = {"q":query}
    header = {"Authorization":f"Bearer {access_token}"}

    response = rqs.get(f"{instance_url}/services/data/v67.0/query", headers=header, params=param)
    print(f"Status: {response.status_code}")
    print(f"Total records: {response.json()['totalSize']}")
    
    orders = response.json()["records"]
    jlpQuant = {}
    bqQuant = {}
    i = 0
    for order in orders:
        
        if order["OrderItems"]:
            for product in order["OrderItems"]["records"]:
                prod_name = product["Product2"]["Name"]
                qty = product["Quantity"]
                account = order["Account"]["Name"]
                if "870L / Black" in prod_name and account == "B&Q Marketplace":

                # if account == "John Lewis D2C":
                #     jlpQuant[prod_name] = jlpQuant.get(prod_name, 0) + qty
                # elif account == "B&Q Marketplace":
                    bqQuant[prod_name] = bqQuant.get(prod_name, 0) + qty




    return jlpQuant,bqQuant



