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
        for i,(k,v) in enumerate(order["products"].items()):
            if k in dxProds or (k in knProds and surcharge()):
                num = dx.tracking(k,order)
            elif k in pfProds:
                num = pf.tracking(k,order)
            else:
                num = kn.tracking(k, order)
            
            try:
                order["tracking_number"] += f"+ {num}"
            except Exception:
                order["tracking_number"] = f"{num}"
    