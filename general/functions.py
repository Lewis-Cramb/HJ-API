from datetime import date as date, timedelta as td, datetime as dt
import base64, emails
from general.productNames import miraklToSF, vsToSF, sfToXero
from general.surchargePostcodes import codes as surCodes

def oldHeader(filename): #Use this function if you do not need the "bearer" in the auth key (So older APIs without OAuth 2.0)
    with open(f"txts/{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"{token}"}

def headerGeneration(filename): #This function generates the headers needed for the JWT (JSON Web Token)
    with open(f"{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"Bearer {token}"}

def vsHeader(): #this function generates the header for virtualstock
    with open("txts/vsUsername.txt", "r") as rf:
        username = rf.read().strip()
    with open("txts/vsPassword.txt", "r") as rf:
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
    
def xeroDue():
    today = date.today()
    due = today + td(days=60)
    return due.strftime("%Y-%m-%d")
    


def printOrders(orders): #This function is used to print the orders just to debug them
    for order in orders:
        print(f"On {order["orderDate"]} and from {order["accName"]}, {order["custName"]} ({order["custPO"]}) ordered:")
        for product in order["products"]:
            print(f"{order["products"][product]}x {product}")
        print(f"For a total of {order["cost"]}")
        print(f"This is to be delivered by {order["shipName"]} by {order["expDate"]}")
        print("\n")


def convertNames(data, source): #this function is used to change the names of products
    if "B&Q" in source:
        conversion = miraklToSF
    elif source == "JLP":
        conversion = vsToSF
    elif source == "SF":
        conversion = sfToXero
    for order in data:
        order["products"] = {
            conversion.get(cleaned_name, cleaned_name): qty
            for name, qty in order["products"].items()
            for cleaned_name in [name if "#" not in name else name.replace("#", "")]
        }
    
    return data

def removeTitles(data):
    for order in data:
        if "Mr " in order["custName"]:
            order["custName"] = order["custName"].partition("Mr ")[2]
        elif "Mrs " in order["custName"]:
            order["custName"] = order["custName"].partition("Mrs ")[2]
        elif "Ms " in order["custName"]:
            order["custName"] = order["custName"].partition("Ms ")[2]
        elif "Dr " in order["custName"]:
            order["custName"] = order["custName"].partition("Dr ")[2]
    return data

def sendEmail(title, body, to="help@haywardjardine.co.uk", report=False):

    fullBody = f"Hi, \n {body} \n \n LewisBot \n\n (You can reply to this email, it is my personal and will always work)"
    fullTitle = f"LewisBot HJ API - {title}"

    password = open("txts/emailPassword.txt","r").read().strip()

    message = emails.html(
        text=fullBody, 
        subject=fullTitle, 
        mail_from=("Lewis", "lewiscramb@icloud.com")
    )

    if report:
        message.attach(
            filename="SalesReport.xlsx",
            data=open("excel/SalesReport.xlsx","rb")
        )
        message.attach(
            filename="StockLevels.xlsx",
            data=open("excel/StockLevels.xlsx","rb")
        )

    message.send(
        to=to,
        smtp={"host": "smtp.mail.icloud.com","port": 587,"tls": True,"user": "lewiscramb@icloud.com","password": password})


def shippingPostcodes(location):
    post_code = location["post_code"]
    area_code = ""
    for letter in post_code:
        if letter.isalpha():
            area_code += letter
        else:
            break

    return area_code in surCodes

def date_format(date):
    day = date.day
    month = date.strftime("%B")
    
    suffix = get_suffix(day)
    
    return f"{day}{suffix} {month}"

def get_suffix(day):
    if day in [1, 21, 31]:
        return "st"
    elif day in [2, 22]:
        return "nd"
    elif day in [3, 23]:
        return "rd"
    else:
        return "th"

def week_range():
    today = dt.now().date()

    start_date = today - td(days=today.weekday())
    end_date = start_date + td(days=6)
    
    start_formatted = date_format(start_date)
    end_formatted = date_format(end_date)
    
    if start_date.month == end_date.month:
        return f"{start_date.day}{get_suffix(start_date.day)}-{end_date.day}{get_suffix(end_date.day)} {start_date.strftime('%b')}"
    else:
        return f"{start_formatted} - {end_formatted}"
