import requests as rqs
import os, shutil
from datetime import datetime as dt, timedelta as td
import sys
sys.path.append("../hj-api")
from general.employees import employeeList as employees

def getToken():
    data = {
        "client_id": open("txts/msID.txt").read().strip(),
        "client_secret": open("txts/msSec.txt").read().strip(),
        "grant_type":"client_credentials",
        "scope":"https://graph.microsoft.com/.default"
    }
    tenantId = open("txts/msTen.txt").read().strip()
    response = rqs.post(f"https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token", data=data)
    return response.json()["access_token"]

def getDriveID(email):
    header = {"Authorization": f"Bearer {getToken()}"}
    response = rqs.get(f"https://graph.microsoft.com/v1.0/users/{email}/drive/root/children", headers=header)
    json = response.json()
    return json["value"][0]["parentReference"]["id"]

def downloadFiles(root_id, emp, local_path):
    os.makedirs(f"{local_path}/{emp}", exist_ok=True)

    header = {"Authorization": f"Bearer {getToken()}"}
    response = rqs.get(f"https://graph.microsoft.com/v1.0/users/{emp}@haywardjardine.co.uk/drive/items/{root_id}/children", headers=header)
    items = response.json()["value"]

    for item in items:
        item_path = os.path.join(f"{local_path}/{emp}", item["name"])
        if "folder" in item:
            downloadFiles(item["id"], emp, item_path)
        else:
            download_url = item.get("@microsoft.graph.downloadUrl")
            if download_url:
                file_response = rqs.get(download_url)
                with open(item_path, "wb") as wb:
                    wb.write(file_response.content)
                print(f"Downloaded: {item_path}")
            else:
                print(f"Skipped (no download URL): {item_path}")




def employeeBackups():
    path = f"D:/backups/{dt.now().strftime("%Y-%m-%d")}"
    oldPath = f"D:/backups/{(dt.now()-td(days=2)).strftime("%Y-%m-%d")}"
    shutil.rmtree(oldPath)
    for employee in employees:
        root_id = getDriveID(f"{employee.lower()}@haywardjardine.co.uk")
        downloadFiles(root_id, employee.lower(), path)