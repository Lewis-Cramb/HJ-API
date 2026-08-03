#this file will be used to create an order on parcelforce and return the tracking number
import requests as rqs
from general.parcelforceItems import Box, Cushion

def getToken(client_id, client_secret):
    payload = {
        "grant_type": "client_credentials",
        "scope": "public-api payment",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    token = rqs.post("https://www.parcel2go.com/auth/connect/token", data=payload)    
    return token.json()["access_token"]

def tracking(product,order):
    clientID = open("txts/pfID.txt").read().strip()
    clientSec = open("txts/pfSec.txt").read().strip()

    headers = {
        "Authorization": f"Bearer {getToken(clientID,clientSec)}",
        "Content-Type": "application/json"
    }
    if " " in order["custName"]:
        first = order["custName"].partition(" ")[0]
        last =  order["custName"].partition(" ")[2]
    else:
        first = "Mx"
        last = order["custName"]

    if "270L" in product:
        item = Box()
    else:
        item = Cushion()

    parcels = []
    parcel = {
        "Height" : item.getHeight(),
        "Length" : item.getLength(),
        "EstimatedValue" : 10,
        "Weight" : item.getWeight(),
        "Width" : item.getWidth(),
        "DeliveryAddress" : {
            "ContactName" : order["custName"],
            "Email" : "help@haywardjardine.co.uk",
            "Phone" : order["custPhone"],
            "Property" : order["shipping_address"]["address_1"],
            "Street" : order["shipping_address"]["address_2"],
            "Town" : order["shipping_address"]["city"],
            "Postcode" : order["shipping_address"]["post_code"],
            "CountryIsoCode" : "GBR",
        },
        "Contents" : [
            {
            "Description" : product,
            "Quantity" : 1,
            "Value" : order["cost"]
            }
        ],
        "ContentsSummary" : product
    }

    for i in range(0, order["products"][product]):
        parcels.append(parcel)

    itemID = order["custPO"].replace("-","")
    remaining = 32-len(itemID)
    for j in range (0,remaining):
        itemID += "0"
    num, cur, id = 0,0, ""
    for char in itemID:
        id += char
        cur += 1
        if (num == 0 and cur == 8) or (cur==4 and (num==1 or num==2 or num==3)):
            id += "-"
            num += 1
            cur = 0


    payload = {
        "Items": [{
            "Id" : id, 
            "Service" : "parcelforce-express-48",
            "OriginCountry" : "GBR",
            "Parcels" : parcels,
            "CollectionAddress" : {
                "ContactName" : order["custName"],
                "Organisation" : "Hayward Jardine",
                "Email" : "help@haywardjardine.co.uk",
                "Phone" : order["custPhone"],
                "Property" : "39",
                "Street" : "Montrose",
                "Town" : "Hillington",
                "County" : "Glasgow",
                "Postcode" : "G52 4LA",
                "CountryIsoCode" : "GBR",
            }
        }],
        "CustomerDetails" : {
            "Email" : "help@haywardjardine.co.uk",
            "Forename" : first,
            "Surname" : last
        }
    }

    response = rqs.post("https://www.parcel2go.com/api/orders",json=payload,headers=headers)
    return response.json()["Links"]["payment"]
