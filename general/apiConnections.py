#This is the main file that is going to be used for GETting, POSTing and everything inbetween
from dataPOST import POSTsf
from general.functions import printOrders as printing, convertNames as conversion, removeTitles as titles
from shippingCalls.shipping import shipping as ship, parseShipping as parse
from invoicing.POSTxero import postData as xero
from copy import deepcopy as dc
import dataPOST.WRITEorders as xlsx


def transfer(sources, key, knPOs, pfPOs, dxPOs, sfPOs):
    data, line_part = sources[key]
    if data != []:
        data = conversion(data, key)

        #shipping
        parse(data, key)
        kn, pf, dx = ship(data, key, line_part)
        knPOs += kn
        pfPOs += pf
        dxPOs += dx

        #invoicing    
        copyData = dc(data)
        copyData = conversion(copyData, "SF")
        for order in copyData:
            if key == "JLP":
                xero(order)

        #salesforce
        data = titles(data)
        printing(data)
        xlsx.upload(data)
        sf = POSTsf.postAPI(data)
        sfPOs += sf

    return knPOs, pfPOs, dxPOs, sfPOs


