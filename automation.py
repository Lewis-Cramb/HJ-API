#This script will be the main script ran, it will keep track of the time too
from datetime import datetime as dt
from general.apiConnections import transfer as automate
from general.functions import sendEmail as email
import infoGet.GETmirakl as mir, infoGet.GETvirtual as vs
from excel.WRITExlsx import update as report


sources = {"B&Qhj":mir.getM("HJ"), "B&Qb":mir.getM("Buffalo"), "JLP":vs.getVS()}
current_day = dt.now().strftime("%A")
sfPOs, knPOs, pfPOs = [],[],[]
if current_day not in ["Saturday", "Sunday"]:
    for index,(key,value) in enumerate(sources.items()):
        sfPOs, knPOs, pfPOs = automate(sources, key, sfPOs, knPOs, pfPOs)

        send, title, body = False, "Daily update", ""

        if sfPOs != []:
            send = True
            body += f"Here are the POs of orders that do not have products in the pricebook (e.g outdoor edit cushions) so need to be made on SalesForce:\n"
            for po in sfPOs:
                body += f"{po}\n"
        if knPOs != []:
            send = True
            body += f"Here are the POs of orders that need to have orders created in Kinetic for them: \n"
            for po in knPOs:
                body += f"{po}\n"
        if pfPOs != []:
            send = True
            body += "Below are the POs of orders needing to be created on ParcelForce, remember to update SalesForce with the tracking numbers:\n"
            for po in pfPOs:
                body += f"{po}\n"

    if send:
        email(title, body, "help@haywardjardine.co.uk")


if current_day == "Monday":
    report()


