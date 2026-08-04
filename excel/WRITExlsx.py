import openpyxl as xlsx
import sys
sys.path.append("../HJ-API")
from general.xlsxRows import rows
from general.functions import week_range, sendEmail as email
import excel.GETquantities as quant

def update():
    jlpQuant, bqQuant = quant.pullSF()
    workbook = xlsx.load_workbook("excel/SalesReport.xlsx")
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

    workbook.save("excel/SalesReport.xlsx")

    email("Sales report", "See the attached sales report", "lewis@haywardjardine.co.uk",True)

update()