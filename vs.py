#this file will be for testing the VS sandbox
import requests as rqs
import base64

username = open("txts/vsUsername.txt","r").read().strip()
password = open("txts/vsPassword.txt","r").read().strip()

# Create Basic Auth header
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
header = {
    "Authorization": f"Basic {credentials}"
}
response = rqs.get("https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json",headers=header,params={"status":"ORDER"})

print(response)
print(response.json())

