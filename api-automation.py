#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import GETmirakl as mir, GETvirtual as vs, POSTsf as sf, cxml as invoice 
from functions import printOrders as printing, convertNames as conversion

def automate(sources, key):
    data,raw = sources[key]
    if key=="JLP":
        invoice.looped(raw)
    data = conversion(data, key)

    printing(data)

    #sf.postAPI(data)


sources = {"B&Q":mir.getM(), "JLP":vs.getVS()}
for index,(key,value) in enumerate(sources.items()):
    automate(sources, key)