# README - VirtualStock Test


This readme is purely for my thoughts and plans for the virtualstock sandbox

# Plan


- GET all orders
- extract data needed to acknowledge orders
- POST an acknowledgement for all orders - completes (new -> processing)
- POST a dispatch for all orders - completes (processing -> dispatched)

# Notes

GET orders - https://api.sandbox.virtualstock.com/restapi/v4/orders/?format=json (order by new => "status" : "ORDER") 

POST acknowledge - https://api.sandbox.virtualstock.com/restapi/v4/orders/ORDER_URI/acknowledge/?format=json (this needs part_number, line_ref and quantity)
POST dispatch - https://api.sandbox.virtualstock.com/restapi/v4/orders/ORDER_URI/dispatch/?format=json (This neds part_number, line_ref, quantity, carrier, supplier_dispatch_date and tracking_number)


To find - what is ORDER_URl


as usual, username and password stored in appropriate txt files in txts/

Maybe ORDER_URl is literally the url of the order when you open it in vs? will test rn
seems likely given what variables are held where (i.e part_number, line_ref and quantity are all stored in response.json()[results][items] instead of just [results])

This hasn't worked, it's getting late so I'm going to leave it for now and come back on 22nd - reckon this is a test or think I'm able to email back to ask questions?


# commit history

a72dd99 - Setup the files

070dd68 - connected to the vs server using credentials

[current commit] - attempting the POST for acknowledging an order (using the first order 230003426)