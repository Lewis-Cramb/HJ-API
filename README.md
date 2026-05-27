# HJ-API
Repo will be used for storing and testing Hayward Jardine REST apis for interlinking systems

# Important Notes

Rate limiting - try not to run any of this manually, it will eat up how much we can pull - leave it to run at 10am each day
Mirakl: 5mins
VS: 250 per min


I cannot test commit [curr num] without the appropriate logins, will need to halt here until I have logins to each service
I will also need to wait until I have seen the TrueCommerce Wickes platform to see if I can implement TrueCommerce - I've added standardised code just in case

# How-To update

You always start by adding the token for the header in a file named "[seller]Token.txt"
Next you need to create the header in sales.py the same way that the others are made by running it through headerGeneration, adding the type if it is for a POST request
You then use request.GET() or request.POST() to complete API call.

# Plan

<ins>27/05/2026</ins> 

The plan is to use the request library to get/post the needed data - I also will now need to deal with the invoices
request.GET(VirtualStock) then request.POST(SalesForce)
GET systems: VirutalStock (https://api-docs.virtualstock.com/), Mirakl, TrueCommerce
POST: SalesForce, Delivery Couriers, Xero, Coupa(?)

For VS we can use a GET for a list of orders, can't do this after each acknowledge but could automate this at, say, 10am? 
Automatically send a GET request through the REST API at 10am to recieve the data, POSTing to SF etc immediately after?
https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json&status=ORDER_ACK
https://your-instance.mirakl.net/api/orders 



# Commit History

93a2db8 - Set-up the repo

e1c70f3 -  Finished set-up and created a function to create headers for requests, testing on VirtualStock and SalesForce

[commit num] - Completed recieving data from VirtualStock and Mirakl bar filtering (Can't solidify anything until I get logins)
