from Lists.productCarriers import dx as dxProds, kinetic as knProds, parcelforce as pfProds
import POSTs.POSTparcelforce as pf, POSTs.POSTkinetic as kn, POSTs.POSTdx as dx
import sys
sys.path.append("../")
from functions import shippingPostcodes as surcharge

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



def parseShipping(order, channel):
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
    
    if "," in shipDetails["address_1"]:
        shipDetails["address_1"] = shipDetails["address_1"][0:shipDetails["address_1"].index(",")]
    return shipDetails


def shipping(orders, key):
    for order in orders:
        order["shipping_address"] = parseShipping(order, key)
        dxContents, knContents, pfContents = [],[],[]
        for i,(productName,v) in enumerate(order["products"].items()):
            if productName in dxProds or (productName in knProds and surcharge(order["shipping_address"])):
                dx.payload(productName, order, dxContents)
            elif productName in pfProds:
                pf.payload(productName, order, pfContents)
            else:
                kn.payload(productName, order, knContents)

        num = ""    
        if dxContents != []:
            num += f"{dx.tracking(productName, order, dxContents)} "
        
        if pfContents != []:
            num += f"{pf.tracking(productName, order, pfContents)} "

        if knContents != []:
            num += f"{kn.tracking(productName, order, knContents)} "

        order["tracking_number"] = f"{num}"
    