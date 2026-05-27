# HJ-API
Repo will be used for storing and testing Hayward Jardine REST apis for interlinking systems


# How-To update

# Plan

<ins>27/05/2026</ins> 

The plan is to use the request library to get/post the needed data - I also will now need to deal with the invoices
request.GET(VirtualStock) then request.POST(SalesForce)
GET systems: VirutalStock (https://api-docs.virtualstock.com/), Mirakl, TrueCommerce
POST: SalesForce, Delivery Couriers, Xero, Coupa(?)

For VS we can use a GET for a list of orders, can't do this after each acknowledge but could automate this at, say, 10am? 
Automatically send a GET request through the REST API at 10am to recieve the data, POSTing to SF etc immediately after?
https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json&status=ORDER_ACK

# Commit History

93a2db8 - Set-up the repo
[most recent commit] -  Finished set-up and created a function to create headers for requests, testing on VirtualStock and SalesForce
