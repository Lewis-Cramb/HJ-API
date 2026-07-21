#this file will be used to create an order on parcelforce and return the tracking number
import requests as rqs

def getToken(client_id, client_secret):
    payload = {
        "grant_type": "client_credentials",
        "scope": "public-api payment",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    token = rqs.post("https://www.parcel2go.com/auth/connect/token", data=payload)
    print(token.status_code)
    print(token.json())
    
    return token.json()["access_token"]

def tracking(product,order):
    clientID = open("txts/pfID.txt").read().strip()
    clientSec = open("txts/pfSec.txt").read().strip()

    headers = {
        "Authorization": f"Bearer {getToken(clientID,clientSec)}",
        "Content-Type": "application/json"
    }

    parcel = {
        "Height" : 12,
        "Length" : 119,
        "EstimatedValue" : 10,
        "Weight" : 9.6,
        "Width" : 60,
        "DeliveryAddress" : {
            "ContactName" : order["custName"],
            "Email" : order["custEmail"],
            "Phone" : order["custPhone"],
            "Property" : order["shipping_address"]["address_1"].partition(" ")[0],
            "Street" : order["shipping_address"]["address_1"].partition(" ")[2],
            "Town" : order["shipping_address"]["city"],
            "Postcode" : order["shipping_address"]["post_code"],
            "CountryIsoCode" : "GBR",
        },
        "Contents" : [
            {
            "Description" : product,
            "Quantity" : order["products"][product],
            "Value" : order["cost"]
            }
        ],
        "ContentsSummary" : product
    }

    payload = {
        "Items": [{
            "Id" : order["custPO"], 
            "Service" : "parcelforce-express-48",
            "OriginCountry" : "GBR",
            "Parcels" : [parcel],
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
            "Email" : order["custEmail"],
            "Forename" : order["custName"].partition(" ")[0],
            "Surname" : order["custName"].partition(" ")[2]
        }
    }

    response = rqs.post("https://www.parcel2go.com/api/orders",json=payload,headers=headers)
    return response.json()["Links"]["payment"]
