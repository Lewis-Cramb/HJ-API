from productCarriers import dx as dxProds, kinetic as knProds
import POSTparcelforce as pf, POSTkinetic as kn, POSTdx as dx

general = ["address_1", "address_2", "post_code", "country", "city", "state"]

vsToGen = {
    "line_1":"address_1",
    "line_2":"address_2",
    "postal_code":"post_code",
    "country":"country",
    "city":"city",
    "state":"state"
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
    elif channel == "B&Q":
        raw_shipping = order["customer"]["shipping_address"]
        keys, values = [mklToGen[k] if k in mklToGen else k for k in list(raw_shipping.keys())], list(raw_shipping.values())
        shipDetails = dict(map(lambda k,v:(k,v),keys,values))
    
    return shipDetails


def shipping(order, key):
    for i,(k,v) in enumerate(order["products"].items()):
        if k in dxProds:
            ship_details = parseShipping(order, key)
            num = dx.tracking(k,ship_details)
        elif k in knProds:
            ship_details = parseShipping(order, key)
            num = kn.tracking(k,order)
        else:
            ship_details = parseShipping(order, key)
            num = pf.tracking(k,order)
        
        try:
            order["tracking_number"] += f"+ {num}"
        except Exception:
            order["tracking_number"] = f"{num}"