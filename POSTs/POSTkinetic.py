#this file will be used to create an order on kinetic and return the tracking number
import requests as rqs
from base64 import b64encode as b64
from Lists.kineticPlatform import buffaloProducts as knBuff
from Lists.productNames import sfToKinetic as codes

def payload(product, order, contents):
    contents.append({
        "itemCode": codes[product]
    })

def tracking(product,order):
    if product in knBuff:
        username = open("txts/knBuffUsername.txt").read().strip()
        password = open("txts/knBuffPassword.txt").read().strip()
    else:
        username = open("txts/knHjUsername.txt").read().strip()
        password = open("txts/knHjPassword.txt").read().strip()

    header = {
        "Authorization": f"Basic {b64(f"{username}:{password}".encode()).decode()}",
        "Content-Type" : "application/json",
        "Accept" : "application/json",
    }

    
    data = {"header": {
        "orderReference": "123 - TEST_2",
        "shipName": "TEST SHIP NAME",
        "address1": order["shipping_address"]["address_1"],
        "address2": order["shipping_address"]["address_2"],
        "city": order["shipping_address"]["city"],
        "county": order["shipping_address"]["state"],
        "country": "GB",
        "postCode": order["shipping_address"]["post_code"],
        "landline": "",
        "mobile": order[""],
        "email": "phil.dickens@baumhaus.co.uk",
        "requestSplitDelivery": "N",
        "deliveryRemarks": "",
        "shippingType": "2",
        "serviceLevel": "TWO MAN",
        "collectionShipName": "Home Decor",
        "collectionAddress1": "Test add 1",
        "collectionAddress2": "Test add 2",
        "collectionCity": "Test city",
        "collectionCounty": "Test county",
        "collectionPostCode": "EH25 9NY",
        "collectionLandline": "01282 59839",
        "collectionMobile": "07980836189",
        "collectionEmail": "phil.dickens@baumhaus.co.uk"},
        "lines": [
            {
            "itemCode": "ZAASSC001"
            }
        ]
    }


    response = rqs.post("https://portal.kineticlogistics.co.uk/api/v1/document", json=data, headers=header)
    print(response)
    print(response.text)
    print(response.status_code)

    print()
    