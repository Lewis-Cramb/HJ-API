import requests as rqs
import sys
sys.path.append("../hj-api")
from general.functions import onedriveToken as token

def backupFiles():
    headers = {"Authorization":f"Bearer {token()}"}