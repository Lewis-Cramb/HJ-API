#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import POSTs.POSTsf as sf
from functions import printOrders as printing, convertNames as conversion, removeTitles as titles
from Couriers.shipping import shipping as ship, parseShipping as parse
from POSTs.POSTxero import postData as xero
from copy import deepcopy as dc


def transfer(sources, key):
    data = sources[key]
    if data != [] and key != "B&Qb":
        data = conversion(data, key)

        #shipping
        parse(data, key)
        ship(data)

        #invoicing    
        copyData = dc(data)
        copyData = conversion(copyData, "SF")
        for order in copyData:
            if key == "JLP":
                xero(order, key)

        #salesforce
        data = titles(data)
        printing(data)
        sf.postAPI(data)


