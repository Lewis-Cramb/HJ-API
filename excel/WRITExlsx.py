import openpyxl as xlsx
import sys
sys.path.append("../HJ-API")
from general.rowNums import rows
import excel.GETquantities as quant
from datetime import datetime as dt, timedelta as td

def week_range():
    today = dt.now().date()

    start_date = today - td(days=today.weekday())
    end_date = start_date + td(days=6)  # Sunday
    
    def format_date(date):
        day = date.day
        month = date.strftime("%B")
        
        suffix = get_suffix(day)
        
        return f"{day}{suffix} {month}"
    
    start_formatted = format_date(start_date)
    end_formatted = format_date(end_date)
    
    # If same month: "3rd-9th Aug"
    if start_date.month == end_date.month:
        return f"{start_date.day}{get_suffix(start_date.day)}-{end_date.day}{get_suffix(end_date.day)} {start_date.strftime('%b')}"
    else:
        # Different months: "27th July - 2nd Aug"
        return f"{start_formatted} - {end_formatted}"

def get_suffix(day):
    if day in [1, 21, 31]:
        return "st"
    elif day in [2, 22]:
        return "nd"
    elif day in [3, 23]:
        return "rd"
    else:
        return "th"

def update():
    jlpQuant, bqQuant = quant.pullSF()
    workbook = xlsx.load_workbook("excel/D2C SALES TRACKER AND FORECAST.xlsx")
    sheet = workbook.active
    dateRange = week_range()

    for i,cell in enumerate(sheet[20]):
        if cell.value == dateRange:
            dateCol = sheet[20][i-1].column_letter
            break

    #jlp
    for product in jlpQuant:
        if product in rows:
            sheet[f"{dateCol}{rows[product][0]}"] = jlpQuant[product]

    #b&q
    for product in bqQuant:
        if product in rows:
            sheet[f"{dateCol}{rows[product][1]}"] = bqQuant[product]

    workbook.save("excel/D2C SALES TRACKER AND FORECAST.xlsx")


update()
