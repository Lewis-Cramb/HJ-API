#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import POSTsf as sf, cxml as invoice 
from functions import printOrders as printing, convertNames as conversion

def transfer(sources, key):
    data,raw = sources[key]
    if key=="JLP":
        invoice.looped(raw)
    data = conversion(data, key)

    printing(data)

    sf.postAPI(data)


