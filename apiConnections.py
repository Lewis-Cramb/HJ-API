#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import POSTsf as sf
from functions import printOrders as printing, convertNames as conversion

def transfer(sources, key):
    data,raw = sources[key]
    
    '''
    data = track(data)

    for order in raw
        inv_num = xero(order)    
        if key = jlp then
            coupa(raw, inv_num)
    '''

    data = conversion(data, key)

    printing(data)

    sf.postAPI(data)


