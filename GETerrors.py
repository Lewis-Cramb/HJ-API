import emails
from GETmirakl import getM

def handle(response):

    if response.status_code >= 200 and response.status_code <= 204: #all success codes
        return "success"
    
    if response.status_code == 400:
        sendEmail("Invalid data", f"Status code: {response.status_code}\nThe data in today's sweep has contained something invalid to the API. You'll need to manually input the data today, sorry :( )")
    elif response.status_code == 401:
        return "Try again"
    elif response.status_code == 403 or response.status_code == 404:
        sendEmail("Can't access", f"Status code: {response.status_code}\nThe api has been denied by the system or the system cannot be found, this needs to be addressed ASAP")
    elif response.status_code == 406:
        sendEmail("Wrong header", f"Status code: {response.status_code}\nThe header isn't working correcetly, this also needs to be addressed ASAP")
    elif response.status_code == 410:
        sendEmail("Disabled API", f"Status code: {response.status_code}\nThe api connection has been terminated at a system level, contact ASAP")
    elif response.status_code == 429:
        #refresh
        return "Try again"
    
    return "failure"


def sendEmail(title, body):

    fullBody = f"Rebecca, \n {body} \n \n LewisBot \n\n (You can reply to this email, it is my personal and will always work)"
    fullTitle = f"LewisBot HJ API - {title}"

    password = open("txts/emailPassword.txt","r").read().strip()

    message = emails.html(
        text=fullBody, 
        subject=fullTitle, 
        mail_from=("Lewis", "lewiscramb@icloud.com")
    )

    response = message.send(
        to="rebecca@haywardjardine.co.uk",
        cc=["emma@haywardjardine.co.uk","alistair@haywardjardine.co.uk"],
        smtp={"host": "smtp.mail.icloud.com","port": 587,"tls": True,"user": "lewiscramb@icloud.com","password": password})