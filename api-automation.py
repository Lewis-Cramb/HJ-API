#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import GETmirakl as  mir, GETvirtual as vs
import POSTsf as sf
from functions import printOrders as printing, convertNames as conversion

def automate(sources, key):
    data = sources[key]

    data = conversion(data, key)

    printing(data)

    #sf.postAPI(data)


sources = {"B&Q":mir.getM(), "JLP":vs.getVS()}
for index,(key,value) in enumerate(sources.items()):
    automate(sources, key)