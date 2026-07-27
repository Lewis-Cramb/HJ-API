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
    if current_day not in ["Saturday","Sunday"] and current_time == "09:30:00":
        knPOs, pfLinks = [],[]
        try:
            for index,(key,value) in enumerate(sources.items()):
                knPOs, pfLinks = automate(sources, key, knPOs, pfLinks)

                send, title, body = False, "Daily update", ""

                if knPOs != []:
                    send = True
                    body += f"Here are the POs of orders that need to have orders created in Kinetic for them: \n"
                    for po in knPOs:
                        body += f"{po}\n"
                if pfLinks != []:
                    send = True
                    body += "Below are the links to pay for orders placed on ParcelForce, remember to update SalesForce with the tracking numbers:\n"
                    for link in pfLinks:
                        body += f"{link}\n"

                if send:
                    email(title, body)
        except Exception:
            email("Crash", "The automation has crashed - data will need to be manually entered")
            print("Not worked")

