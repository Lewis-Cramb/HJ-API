#This file is going to be for reading all of the data
import requests as rqs
import datetime as dt
from datetime import timedelta

workingDate = dt.datetime.now().strftime("%A")

def headerGeneration(filename): #This function generates the headers needed for the JWT (JSON Web Token)
    with open(f"{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"Bearer {token}"}

def oldHeader(filename): #Use this function if you do not need the "bearer" in the auth key (So older APIs without OAuth 2.0)
    with open(f"{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"{token}"}


def getAPIs():

    #Define the commerce platform header here (i.e VirtualStock, Mirakl, TrueCommerce)
    vs_headers = headerGeneration("vsToken")
    mkl_headers = oldHeader("mklToken")


    #All calls will need parameters so you can create a dictionary and add them here
    vs_params = {"status":"ORDER_ACK"}
    mkl_params = {"start_date":dt.datetime.now()-timedelta(1), "end_date":dt.datetime.now()} #Get all orders from yesterday
    if workingDate == "Monday": #Subtract 3 days from the start if its a monday due to weekend orders (i.e friday-sunday)
        mkl_params["start_date":dt.datetime.now()] = timedelta(3)

    #Call APIs using rqs.get() to get the data
    vs_resp = rqs.get("https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json",headers=vs_headers, params=vs_params) #Get all acknowledged orders from VirtualStock
    mkl_resp = rqs.get("https://your-instance.mirakl.net/api/orders",headers=mkl_headers, params=mkl_params)

    #Finally, filter it and join it all together

    #I need the customer name, customer address, order date, courier details including tracking number, and product - also need to send the name of the seller

    #virtualstock - filter this by date too

    return filtered_data

