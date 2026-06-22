from datetime import date as date, timedelta as td, datetime as dt
import base64

def oldHeader(filename): #Use this function if you do not need the "bearer" in the auth key (So older APIs without OAuth 2.0)
    with open(f"txts/{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"{token}"}

def headerGeneration(filename): #This function generates the headers needed for the JWT (JSON Web Token)
    with open(f"{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"Bearer {token}"}

def vsHeader():
    with open("vsUser.txt", "r") as rf:
        username = rf.read().strip()
    with open("vsPass.txt", "r") as rf:
        password = rf.read().strip()

    credentials = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}


      

def startDate(): #This function is used for filtering data to be relevant and un-entered on SF
    if date.today().strftime("%A") == "Monday":
        return date.today()-td(days=3)
    return date.today()-td(days=1)


def format_date(raw_date): #this function is used to convert the date into yyyy-mm-dd
    try:
        return dt.strptime(raw_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        return dt.strptime(raw_date, "%d-%m-%Y").strftime("%Y-%m-%d")
    


def printOrders(orders): #This function is used to print the orders just to debug them
    for order in orders:
        print(f"On {order["orderDate"]}, {order["custName"]} ({order["custPO"]}) ordered:")
        for product in order["products"]:
            print(f"{order["products"][product]}x {product}")
        print(f"For a total of {order["cost"]}")
        print(f"This is to be delivered by {order["shipName"]} by {order["expDate"]}")
        print("\n")