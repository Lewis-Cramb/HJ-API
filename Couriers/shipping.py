from Lists.productCarriers import dx as dxProds, kinetic as knProds, parcelforce as pfProds
from Lists.dxPlatform import HJ, DT
import POSTs.POSTparcelforce as pf, POSTs.POSTdx as dx
import sys
sys.path.append("../")
from functions import shippingPostcodes as surcharge, sendEmail as email

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
    knPOs, pfLinks = [],[]
    for order in orders:
        order["shipping_address"] = parseShipping(order, key)
        dxContentsHJ, dxContentsDT  = [],[]
        for i,(productName,v) in enumerate(order["products"].items()):
            if productName in dxProds or (productName in knProds and surcharge(order["shipping_address"])):
                if productName in HJ:
                    dx.payload(productName, order, dxContentsHJ)
                elif productName in DT:
                    dx.payload(productName, order, dxContentsDT)
            elif productName in pfProds:
                pfLinks.append(f"{pf.tracking(productName, order)}")
            else:
                knPOs.append(order["custPO"])

        # num = ""
        # if dxContentsHJ != []:
        #     num += f"{dx.tracking("HJ", order, dxContentsHJ)} "

        # if dxContentsDT != []:
        #     num += f"{dx.tracking("DT", order, dxContentsDT)} "    
        
        # order["tracking_number"] = f"{num[:-1]}"


    send, title, body = False, "Daily update", ""

    if knPOs != []:
        send = True
        body += "Here are the POs of orders on SalesForce that need to have orders created in Kinetic for them: \n"
        for po in knPOs:
            body += f"{po}\n"
    

    if pfLinks != []:
        send = True
        body += "Below are the links to pay for orders placed on ParcelForce, remember to update SalesForce with the tracking numbers:\n"
        for link in pfLinks:
            body += f"{link}\n"

    print(body)
    return 
    if send:
        email(title, body)
    