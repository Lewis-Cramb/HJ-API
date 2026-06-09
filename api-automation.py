#This is the main file that is going to be used for GETting, POSTing and everything inbetween
import GETmirakl as  mir, GETvirtual as vs
import POSTing as sf
from functions import printOrders as printing
from productNames import miraklToSF


bnq_data = mir.getM()
#vs_data = vs.getVS()

printing(bnq_data)

print("\n changed names \n")

for order in bnq_data:
    order["products"] = {
        miraklToSF.get(name, name): qty
        for name, qty in order["products"].items()
    }

printing(bnq_data)

sample = [bnq_data[0]]
sample[0]["custName"] = "LEWIS-TEST-2"
sample[0]["custPO"] = "123456789987654323"


sf.postAPI(sample)

