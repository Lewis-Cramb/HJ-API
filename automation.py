#This script will be the main script ran, it will keep track of the time too
from datetime import datetime as dt
from apiConnections import transfer as automate
from functions import sendEmail as email
import GETs.GETmirakl as mir, GETs.GETvirtual as vs


sources = {"B&Qhj":mir.getM("HJ"), "B&Qb":mir.getM("Buffalo"), "JLP":vs.getVS()}
sfPOs, knPOs, pfLinks = [],[],[]

for index,(key,value) in enumerate(sources.items()):
    sfPOs, knPOs, pfLinks = automate(sources, key, sfPOs, knPOs, pfLinks)

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
    if pfLinks != []:
        send = True
        body += "Below are the links to pay for orders placed on ParcelForce, remember to update SalesForce with the tracking numbers:\n"
        for link in pfLinks:
            body += f"{link}\n"

    if send:
        email(title, body)


