import requests

url = "https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
