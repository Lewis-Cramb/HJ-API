#This is the main file that is going to be used for GETting, POSTing and everything inbetween
from dataPOST import POSTsf
from general.functions import printOrders as printing, convertNames as conversion, removeTitles as titles
from shippingCalls.shipping import shipping as ship, parseShipping as parse
from invoicing.POSTxero import postData as xero
from copy import deepcopy as dc
import dataPOST.WRITEorders as xlsx

def transfer(sources, key, knPOs, pfPOs, dxPOs, fails):
    data, line_part = sources[key]
    if data != []:
        data = conversion(data, key)
        xlsx.upload(data)
        print()

        # #shipping
        # parse(data, key)
        # kn, pf, dx, failed = ship(data, key, line_part)
        # knPOs += kn
        # pfPOs += pf
        # dxPOs += dx
        # fails += failed

        # #invoicing    
        # copyData = dc(data)
        # copyData = conversion(copyData, "SF")
        # invoiceNumbers = []
        # for order in copyData:
        #     try:
        #         if key == "JLP":
        #             invoiceNumbers = xero(order, invoiceNumbers)
        #     except Exception:
        #         invoiceNumbers.pop()
        #         fails.append(f"{order["custPO"]} - invoicing")

        # #salesforce
        # data = titles(data)
        # printing(data)
        # xlsx.upload(data)
        # failed = POSTsf.postAPI(data)
        # fails += failed

    return knPOs, pfPOs, dxPOs, fails


