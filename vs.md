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