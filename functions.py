from datetime import date as dt, timedelta as td

def oldHeader(filename): #Use this function if you do not need the "bearer" in the auth key (So older APIs without OAuth 2.0)
    with open(f"txts/{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"{token}"}

def headerGeneration(filename): #This function generates the headers needed for the JWT (JSON Web Token)
    with open(f"{filename}.txt") as rf:
        token = rf.read() #Tokens for sales platforms
    return {"Authorization":f"Bearer {token}"}

def startDate():
    if dt.today().strftime("%A") == "Monday":
        return dt.today()-td(days=3)
    return dt.today()-td(days=1)