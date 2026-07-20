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

<ins> 30/06/2026 </ins>

Checked SalesForce and found out how the tracking numbers are stored therefore have started to implement it - will need to pitch ShipTheory and Xero custom connection

Adding the template for tracking numbers is a lot more detail than I thought, needing to add stuff for parsing delivery details as well as changing lots how the raw data is passed back into the apiConnections.py

also added test.py to .gitignore just in case I forget to delete it 


THE PROGRAM IS LIVE - THE CONNECTIONS FROM VS AND MKL TO SF ARE LIVE AND RUNNING

Just had TrueCommerce call, it may not be worth the cost of the API

Also just changed the time from 1000 to 0900 for orders to be pulled through

going to tidy up the repo, too many random python files

<ins> 01/07/2026 </ins>

program didn't work live - issue is the picklist for the delivery couriers so either fix delivery and roll it out all in one or just set it to dx or smth and let others worry about that

Had my call with ShipTheory, they can't give us exactly what we want but we can manage with it

Typically just got an email response from DX now and they have an api that can be used, committing current changes and will switch branches for dx sandbox creds


<ins> 06/07/2026 </ins>

Had my call with TC, they cannot help us

completed the DX sandbox credential stuff - I need to get api credentials for the Davis Turner DX despatch too

Creating the generic DX stuff whilst I wait for the actual creds
Need to ask what the reference is - is it the PO number from SF?

I've just basically refactored the shipping.py file and decided to make a start on filtering the couriers, leading to me starting to plan and design the integration for kinetic as they do not have an api
lead me to emailing the POs of untracked kinetic orders (i.e orders kinetic ship without a surcharge) so that they can be created manually

I don't think I'm going to make the soft deadline of 20/07/2026 given I'm off next week but I am almost there - all that is left is DX credentials for testing, ParcelForce API docs and creds, then Xero creds and testing (subscription bought) and finally coupa creds and testing

<ins> 07/07/2026 </ins>

Need to make adjustments so that we can use buffalo shelving in the automation too

Making a start on Xero now that the custom connection is set up - need to make a list of names:itemCodes so that it can be pulled easily, dont want to do it rn because its tedious BUT DONT FORGET

just got my dx creds and endpoints, accidentally mistyped the warehouse number for DT so gone back to James about that - hopefully he won't be too mad given that he did technically give me their password

Added __init__.py to every folder to mark it as a package, removes the repeat sys.path.append() call when trying to use functions in function.py

kinetic do have an api after all - more work for me


here is the plan:

fix xero -> finalise dx -> write Kinetic API -> find and write parcelforce api -> deal with coupa

Xero GBP Invoice - 60 days terms id is: ff5cbad5-f371-4fd2-a13d-e8ac5e719946

Done everything with xero bar testing and creating the products list

Need a list of names:weights so will do this and the list of names:itemCodes for this commit - prudence told me that the weight is the gross weight rounded up

parsed the rest of the dx info, dx runs fine now - worth nothing that there was no option for 2 day delivery so I've had to opt for 3 day deliveries


<ins> 08/07/2026 </ins>

Off to london for 6 days so need to wrap most stuff up the now if hoping to hit soft deadline of the 20th

DX is done, Xero is tested and done now too (check with emma if she needs the invoice number which is found in xml <Invoices><invoice><invoiceNumber>)
All thats left is Kinetic, ParcelForce and Coupa - Kinetic have given me their docs so that should hopefully make it easier, PF needs some research and coupa is on hold without the creds
I'll be in 16th and 17th so can wrap everything up then too

Okay a little bit stuck, realising I messsed up with DX
Need to email in to clarify but the code I wrote meant that the entire order went onto one DX consignemnt, dont think thats the case - what to do if pf is needed with dx? - emailled so im going to deal with kinetic rn

There isn't much I can do whilst wfh (will probs stop doing it asap), made a start on kinetic

<ins> 09/07/2026 </ins>

It's thursday. I'm also currently on the train to london. Shouldn't be working but need to make note to reply to JLP finance with acc number, think I'll be given the duns and the secret
Need to kill time on this train (trespassers on tracks delayed the train) so may take another look at the kinetic stuff
Keep getting SSL errors because of bad connection, not going to continue - I'll resume on the 16th when I come into the office

<ins> 20/07/2026 </ins>

Right first day back since London - first things first I've not hit the soft deadline of the 20th but I am close

First order of attention is writing kinetic code and emailling JLP back - scratch that the first thing I am doing is writing down in my notebook to remind myself of it all

Getting a 403 with kinetic for both HJ and Buffalo, emailling Hannah now too

Kinetic is waiting on an email, Coupa is waiting on an email
All that's left is to fix DX and start parcelforce

I had to change the customer number in POSTxero.py as they changed on xero

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

8aabb8e - touchups and added the lists for each carrier's products

18718cc - Start of shipping coding AND LIVE CODE

485da34 - Refactored and tidied up again

3e2330b - Made some more changes just before DX

86d1e1d - Boilerplate DX api code

87d03c1 - Kinetic emails

4b11465 - Xero almost complete

8e17af2 - Lists for weights and codes

d7ed175 - Xero tested and finished

[commit num] - Kinetic started