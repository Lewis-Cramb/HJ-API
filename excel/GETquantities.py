import requests as rqs
import sys
from datetime import datetime as dt, timedelta as td
sys.path.append("../HJ-API/")
from dataPOST.POSTsf import getAuthToken as sfAuth
from general.xlsxRows import base
from copy import deepcopy as dc

def pullSF():
    access_token,instance_url = sfAuth()

    today = dt.today().date()
    monday_this_week = today - td(days=today.weekday())
    last_monday = monday_this_week - td(days=7)
    last_sunday = monday_this_week - td(days=1)

    query = f"SELECT Id, OrderNumber, Account.Name, Status, EffectiveDate, (SELECT Id, Product2.Name, Quantity, UnitPrice FROM OrderItems) FROM order WHERE EffectiveDate >= {last_monday} AND EffectiveDate <= {last_sunday} AND (NOT Status LIKE 'New') ORDER BY CreatedDate DESC LIMIT 10000"

    param = {"q":query}
    header = {"Authorization":f"Bearer {access_token}"}

    response = rqs.get(f"{instance_url}/services/data/v67.0/query", headers=header, params=param)
    
    orders = response.json()["records"]
    jlpQuant, bqQuant = dc(base), dc(base)
    jlpTotal, bqTotal, totalUnits = 0,0,0
    for order in orders:
        if order["OrderItems"]:
            for product in order["OrderItems"]["records"]:
                prod_name = product["Product2"]["Name"]
                qty = product["Quantity"]
                account = order["Account"]["Name"]
                price = product["UnitPrice"]
                totalUnits += qty
                if account == "John Lewis D2C" and prod_name in base:
                    jlpQuant[prod_name] += qty
                    jlpTotal += price*qty
                elif account == "B&Q Marketplace" and prod_name in base:
                    bqQuant[prod_name] += qty
                    bqTotal += price*qty


    return jlpQuant, bqQuant, jlpTotal, bqTotal, totalUnits