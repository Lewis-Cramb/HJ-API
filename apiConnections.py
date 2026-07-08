#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import POSTs.POSTsf as sf
from functions import printOrders as printing, convertNames as conversion
from Couriers.shipping import shipping as ship
from POSTs.POSTxero import postData as xero
from copy import deepcopy as dc


def transfer(sources, key):
    data = sources[key]
    if data != []:
        data = conversion(data, key)

        #ship(data, key)

        copyData = dc(data)
        copyData = conversion(copyData, "SF")
        for order in copyData:
            xero(order, key)           

        printing(data)

        #sf.postAPI(data)


