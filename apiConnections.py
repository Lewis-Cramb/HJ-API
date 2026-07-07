#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import POSTs.POSTsf as sf
from functions import printOrders as printing, convertNames as conversion
from Couriers.shipping import shipping as ship
from POSTs.POSTxero import postData as xero


def transfer(sources, key):
    data = sources[key]
    data = conversion(data, key)
    #leftoverPOs = ship(data, key)
    '''
    for order in raw
        inv_num = xero(order)    
        if key = jlp then
            coupa(raw, inv_num)
    '''

    xero(data[0], key)

    print()
    

    printing(data)

    #sf.postAPI(data)

    #return leftoverPOs


