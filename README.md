# HJ-API
Repo will be used for storing and testing Hayward Jardine REST apis for interlinking systems

# Important Notes

Rate limiting - try not to run any of this manually, it will eat up how much we can pull - leave it to run at 10am each day
Mirakl: 5mins
VS: 250 per min


I cannot test commit 984d24c or commit 184d741 without the appropriate logins, will need to halt here until I have logins to each service
I will also need to wait until I have seen the TrueCommerce Wickes platform to see if I can implement TrueCommerce - I've added standardised code just in case // (08/06/2026) think TC runs off of virtual stock? can maybe just use it that way?

# How-To update

You always start by adding the token for the header in a file named "[seller]Token.txt" in a folder /txts/.
Then you need to create a new python script for your call, you can copy and paste what I've written if needs be. Then you need to update it for filtering, storing and calling before inputting the data needed in the header etc.

You need to put the comsumer id and consumer secret into to seperate files (sfConsID.txt and sfConsSec.txt) also in /txts/ - these are not updated on the repo so that they are hidden but you can find them in the OAuth settings for LC-AUTO-API on salesforce external client app manager

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

<ins>08/06/2026</ins>

SalesForce has been successfully POSTed to using sales.py
Next step is to refactor the code slightly as I misjudged how big the requests would be
From there I am going to work on VirtualStock, Mirakl, TrueCommerce and then couriers (subject to change)
The last thing I will do are the invoices

<ins>09/06/2026</ins>

Had a few thoughts about the automation last night/this morning - might be easier to create an app or program where you click "run" to transfer everything? I'm not sure where would host the automation as it certainly cannot be me - maybe HJ have a spare laptop that they can just keep on?
Need a new keyboard, 80%? 95%? Needs numpad but not arrow keys - Not important for now

Might book a demo for TC api demo, see if i can just get the ability to request data - I've booked a demo  - dont do anything with TC until finished mirakl and virtual stock, it is the hardest to do

I need to add error handling!!!

Next up is the delivery courier stuff, Emma to chase JL for me for api credentials. Got a laptop so able

<ins> 10/06/2026 </ins>

I am not in today, it is currently 21:22, as I am away on holiday tomorrow
JL SDO got back with sandbox credentials so I've commited the error handling stuff when it is partially complete, still need to account for 429 and deal with emails properly

The sandbox will be tested and work, I will make a seperate python file to do so - will commit on seperate branch

<ins> 22/06/2026 </ins>

I did VS credential stuff, only took about an hour total

Next up is starting to take a look at the delivery platforms, seeing how to link to them (if possible) - I've contacted Kinetic to see if it is possible, can make a start on DX right now

For DX I can't do much right now as I don't know enough - will circle back to this and make a start on the invoicing side

XERO needs an extra subscription for the automation to work, not sure of price yet but will write the implementation code and find price after
https://developer.xero.com/documentation/guides/oauth2/custom-connections

I am not able to do much this week, I need logins and verifications but people are OOO so I can't get that

Done some digging for deliveries, found a system called ShipStation API that works for DX and for ParcelForce in one, £59 per month

<ins> 23/06/2026 </ins>

Got my VS credentials from JLP so spending today testing

Took a minute but got connected, forgot that the http wouldnt need .sanbox - all working now - - also parsed all of the data correctly, the program can now successfully link virtualstock to salesforce!

I need to use cXML for coupa's invoices, going to make a start on learning how to use cxml in python - i dont have credentials (not too sure how to get tbh) so make boilerplate cxml creation and connection

<ins> 24/06/2026 </ins>

Looking at automation, seeing how to run the code without needing to press F5

Timezones should be automatically accounted for, no need to fiddle with that - may try to make the automation.py file an exe later down the line but for now it is fine as .py

Doing more cxml, PayloadID in "<DocumentReference>" is just the Supplier Order Number, date format is ISO - need to get our DUNS, buyer DUNS, and client secret

<ins> 29/06/2026 </ins>

Got logins for Xero so going to make a start there - I've emailed JL about the cxml in coupa stuff so will see

Found company duns using a website

Lots of reading today, found an OpenAPI for ParcelForce so may start to implement the courier stuff - need to have someone go over how we use parcelforce though before this

I've done some finetuning, added things such as our DUNS number and the lists for which carrier does what

# Commit History

93a2db8 - Set-up the repo

e1c70f3 - Finished set-up and created a function to create headers for requests, testing on VirtualStock and SalesForce

984d24c - Completed recieving data from VirtualStock and Mirakl bar filtering (Can't solidify anything until I get logins)

184d741 - Added the link to SalesForce, not tested

7fd28f5 - I've now testing and perfected the salesforce link, data can now properly be POSTed to SF

9b1760b - Refactoring, cleaner and shorter python scripts and all text files held in a folder /txt/

ec0a88a - Added the filtering to the GET requests, still can't test them until JL/VS get back

7dac154 - Tested the GET request for Mirakl, works perfectly

c3154f1 - Refactored once again, splitting functions - the GET file kept growing

4313527 - Tested the Mirakl to Salesforce integration directly, works exactly as planned 

c8f54df - Added error handling almost fully

3e9b41e - Added VS product names and tidied stuff up

c0a9f66 - Finished error handling for the GETs

4126be4 - Added boilerplate Xero integration

3a8fd3c - Connected to VirtualStock using credentials

e4c1fb9 - VirtualStock data fully passes through to SalesForce

57ac2d8 - Added boilerplate cxml for integration with coupa

df2ae04 - Created the scripting for autonomously running the project

9a83284 - Increased CXML, filled out more data for it - still can't test it

[commit num] - touchups and added the lists for each carrier's products