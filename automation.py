#This script will be the main script ran, it will keep track of the time too
from datetime import datetime as dt
from apiConnections import transfer as automate
from functions import sendEmail as email
import GETs.GETmirakl as mir, GETs.GETvirtual as vs

while True:
    now = dt.now()
    current_time = now.strftime("%H:%M:%S")
    current_day = now.strftime("%a")
    sources = {"B&Qhj":mir.getM("HJ"), "B&Qb":mir.getM("Buffalo"), "JLP":vs.getVS()}
    if current_day not in ["Saturday","Sunday"] and current_time == "09:00:00":
        try:
            for index,(key,value) in enumerate(sources.items()):
                automate(sources, key)
        except Exception:
            email("Crash", "The automation has crashed - data will need to be manually entered")
            print("Not worked")

