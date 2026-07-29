import time
from general.functions import sendEmail as email

def handle(response):

    if response.status_code >= 200 and response.status_code <= 204: #all success codes
        return "success"
    
    if response.status_code == 400:
        #handled in other email
        pass
    elif response.status_code == 403 or response.status_code == 404:
        email("Can't access", f"Status code: {response.status_code}\nThe api has been denied by the system or the system cannot be found, this needs to be addressed ASAP")
    elif response.status_code == 406:
        email("Wrong header", f"Status code: {response.status_code}\nThe header isn't working correcetly, this also needs to be addressed ASAP")
    elif response.status_code == 410:
        email("Disabled API", f"Status code: {response.status_code}\nThe api connection has been terminated at a system level, contact ASAP")
    elif response.status_code == 429:
        print("Sleeping")
        time.sleep(120)
        return "Try again"

    return "Failure"


