import requests as rqs
import sys
sys.path.append("../hj-api")
from general.functions import getSPToken as getToken
from general.GETerrors import handle

def download(filename="StockSalesSheet.xlsx", spPath="D2C/", path="dataPost/StockSalesSheet.xlsx"):
    token = getToken()
    header = {"Authorization": f"Bearer {token}"}
    response = rqs.get(f"https://graph.microsoft.com/v1.0/me/drive/root:/{spPath}/{filename}:/content", headers=header)

    err = handle(response)
    if err == "Failure":
        return False
    elif err == "Try again":
        return download()

    with open(path, "wb") as wf:
        wf.write(response.content)
    return True

download()
