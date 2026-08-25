#This script will be the main script ran, it will keep track of the time too
from datetime import datetime as dt
from general.apiConnections import transfer as automate
from general.functions import sendEmail as email
from backupOneDrive import employeeBackups as oneDriveBackup
import infoGet.GETmirakl as mir, infoGet.GETvirtual as vs
from excel.WRITExlsx import update as report


sources = {"B&Qhj":mir.getM("HJ"), "B&Qb":mir.getM("Buffalo"), "JLP":vs.getVS()}
current_day = dt.now().strftime("%A")
knPOs, pfPOs, dxPOs, failed = [],[],[],[]
if current_day not in ["Saturday", "Sunday"]:
    for index,(key,value) in enumerate(sources.items()):
        knPOs, pfPOs, dxPOs, failed = automate(sources, key, knPOs, pfPOs, dxPOs, failed)

    send, title, body = False, "Daily update", ""

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
    if dxPOs != []:
        send = True
        body += "Below are POs of orders on SalesForce that need DX consignments created for them: \n"
        for po in dxPOs:
            body += f"{po}\n"

    if failed != []:
        send = True
        body += f"Some orders failed, listed are their POs and where they failed:\n"
        for po in failed:
            body += f"{po}\n"

    if send:
        email(title, body, "help@haywardjardine.co.uk")


    oneDriveBackup()


if current_day == "Monday":
    report()


