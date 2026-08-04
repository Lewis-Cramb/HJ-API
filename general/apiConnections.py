#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import dataPOST.POSTsf as sf
from general.functions import printOrders as printing, convertNames as conversion, removeTitles as titles
from shippingCalls.shipping import shipping as ship, parseShipping as parse
from invoicing.POSTxero import postData as xero
from copy import deepcopy as dc


def transfer(sources, key, sfPOs, knPOs, pfLinks):
    data, line_part = sources[key]
    if data != [] and key == "B&Qhj":
        data = conversion(data, key)

        #shipping
        parse(data, key)
        kn, pf = ship(data, key, line_part)
        knPOs += kn
        pfLinks += pf

        #invoicing    
        copyData = dc(data)
        copyData = conversion(copyData, "SF")
        for order in copyData:
            if key == "JLP":
                xero(order, key)

        #salesforce
        data = titles(data)
        printing(data)
        POs = sf.postAPI(data)
        sfPOs += POs

    return sfPOs, knPOs, pfLinks


