import requests as rqs

def headerGeneration(filename): #This function generates the headers needed for the JWT (JSON Web Token)
    with open(f"{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"Bearer {token}"}

#Define the commerce platform header here (i.e VirtualStock, Mirakl, TrueCommerece)
vs_headers = headerGeneration("vsToken")

#Define the sales data platform header here (i.e SalesForce)
sf_headers = headerGeneration("sfToken")
sf_headers["Content-Type"] = "application/json" #You are making a POST request (giving data) therefore you need to define what format the given data is in

print(vs_headers)
print(sf_headers)