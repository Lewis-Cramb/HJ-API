from general.productCarriers import dx as dxProds, kinetic as knProds
from general.dxPlatform import HJ, DT
import shippingCalls.POSTparcelforce as pf, shippingCalls.POSTdx as dx, shippingCalls.PUTvs as trackVS, shippingCalls.PUTmkl as trackMkl
from general.functions import shippingPostcodes as surcharge

general = ["address_1", "address_2", "post_code", "country", "city", "state"]

vsToGen = {
    "line_1":"address_1",
    "line_2":"address_2",
    "postal_code":"post_code",
    "country":"country",
    "city":"city",
    "state":"state",
    "full_name":"customer_name"
}

mklToGen = {
    "street_1":"address_1",
    "street_2":"address_2",
    "zip_code":"post_code",
    "country":"country",
    "city":"city",
    "state":"state"
}



def parseShipping(orders, channel):
    for order in orders:
        shipDetails = {}
        if channel == "JLP":
            raw_shipping = order["shipping_address"]
            keys, values = [vsToGen[k] if k in vsToGen else k for k in list(raw_shipping.keys())], list(raw_shipping.values())
            shipDetails = dict(map(lambda k,v:(k,v),keys,values))
        elif "B&Q" in channel:
            raw_shipping = order["shipping_address"]
            keys, values = [mklToGen[k] if k in mklToGen else k for k in list(raw_shipping.keys())], list(raw_shipping.values())
            shipDetails = dict(map(lambda k,v:(k,v),keys,values))
            shipDetails["customer_name"] = f"{raw_shipping["firstname"]} {raw_shipping["lastname"]}"
            shipDetails["customer_phone"] = raw_shipping["phone"]

        address = shipDetails["address_1"]
        
        if "," in address and any(char.isdigit() for char in address):
            shipDetails["address_1"] = address.partition(",")[0]
            shipDetails["address_2"] = address.partition(",")[2]
        elif " " in address and any(char.isdigit() for char in address):
            shipDetails["address_1"] = address.partition(" ")[0]
            shipDetails["address_2"] = address.partition(" ")[2]

        order["shipping_address"] = shipDetails

def updateTrackingInfo(order, key, line_part_url):
    if " " in order["tracking_number"]:
        order["tracking_number"] = order["tracking_number"].partition(" ")[0]

    if order["accName"] == "John Lewis D2C":
        trackVS.updateTracking(order, line_part_url)
    elif order["accName"] == "B&Q Marketplace":
        if key == "B&Qb":
            trackMkl.updateTracking(order, "Buffalo")
        elif key == "B&Qhj":
            trackMkl.updateTracking(order, "HJ")

def shipping(orders, key, line_part_url):
    knPOs, pfPOs = [],[]
    for order in orders:
            dxContentsHJ, dxContentsDT  = [],[]
            for i,(productName,v) in enumerate(order["products"].items()):
                if productName in dxProds or (productName in knProds and surcharge(order["shipping_address"])):
                    order["shipName"] = "DX"
                    if productName in HJ:
                        dx.payload(productName, order, dxContentsHJ)
                    elif productName in DT:
                        dx.payload(productName, order, dxContentsDT)
                elif productName in knProds:
                    order["shipName"] = "KINETIC LOGISTICS"
                    knPOs.append(order["custPO"])
                else:
                    order["shipName"] = "Parcel force"
                    pfPOs.append(order["custPO"])

            num = ""
            if dxContentsHJ != []:
                num += f"{dx.tracking("HJ", order, dxContentsHJ)} "

            if dxContentsDT != []:
                num += f"{dx.tracking("DT", order, dxContentsDT)} "    
            
            order["tracking_number"] = f"{num[:-1]}"

            
    dxOrders = [order for order in orders if order["shipName"]=="DX"]
    for dxOrder in dxOrders:
        updateTrackingInfo(dxOrder, key, line_part_url)


    return knPOs, pfPOs
    