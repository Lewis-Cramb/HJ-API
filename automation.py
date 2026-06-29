#This script will be the main script ran, it will keep track of the time too
from datetime import datetime as dt
from apiConnections import transfer as automate
import GETmirakl as mir, GETvirtual as vs

while True:
    now = dt.now()
    current_time = now.strftime("%H:%M:%S")
    current_day = now.strftime("%a")
    if current_day not in ["Saturday", "Sunday"] and current_time == "10:00:00":
        sources = {"B&Q":mir.getM(), "JLP":vs.getVS()}
        for index,(key,value) in enumerate(sources.items()):
            automate(sources, key)

