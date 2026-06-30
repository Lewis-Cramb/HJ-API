#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import POSTs.POSTsf as sf
from Generalisation.functions import printOrders as printing, convertNames as conversion
from Couriers.shipping import shipping as ship


def transfer(sources, key):
    data,raw = sources[key]
    
    for i,order in enumerate(raw):
        data[i]["tracking_number"] = ship(order, key)
    '''
    for order in raw
        inv_num = xero(order)    
        if key = jlp then
            coupa(raw, inv_num)
    '''

    data = conversion(data, key)

    printing(data)

    return
    #sf.postAPI(data)


