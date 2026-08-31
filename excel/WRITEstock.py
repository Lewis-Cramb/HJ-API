import openpyxl as xlsx
from datetime import datetime as dt
import sys
sys.path.append("../HJ-API")
from general.xlsxRows import reorderList
from general.functions import monthToCol, week_range

def reorder(quantities,totals, totalUnits, monthTotal):
    workbook = xlsx.load_workbook("excel/StockLevels_TEST.xlsx")
    sheet = workbook.active

    readWeeks, writeWeeks = ["C","D","E"],["B","C","D"]
    week4s, week3s, week2s = [],[],[]

    colReadWeeks = {"C":week4s,"D":week3s,"E":week2s}
    colWriteWeeks = {"B":week4s,"C":week3s,"D":week2s}

    for col in readWeeks:
        for j,cell in enumerate(sheet[col]):
            if j >= 6 and j <= 20:
                colReadWeeks[col].append(cell.value)

    for col in writeWeeks:
        i = 0 
        for j,cell in enumerate(sheet[col]):
            if j>=7 and j <= 21:
                sheet[f"{col}{j}"] = colWriteWeeks[col][i]
                i += 1 

    row = 7
    for product in reorderList:
        sheet[f"E{row}"] = quantities[product]
        sheet[f"G{row}"] = sheet[f"G{row}"].value - quantities[product]
        row += 1

    sheetNum = 2
    sheets = workbook.sheetnames
    sheetName = sheets[sheetNum]
    sheet = workbook[sheetName]

    sheet["O4"].value = f"£{totals[1]}"
    sheet["P4"].value = f"£{totals[2]}"
    sheet["Q4"].value = f"£{totals[0]}"


    if sheet["U16"].value > sheet["U13"].value:
        sheet["U13"].value = sheet["U16"].value
        sheet["T13"].value = sheet["T16"].value

    sheet["U16"].value = totalUnits
    sheet["T16"].value = week_range()

    matrix = {}
    for row in sheet:
        for cell in row:
            matrix[cell.value] = f"{cell.column_letter}{cell.row+1}"
    

    sheet["Y12"].value = sheet[matrix[week_range()]].value

    sheet[matrix[week_range()]].value = sheet["U16"].value

    
    if dt.today().day <= 7: 
        if dt.today().month == 2:
            monthNums = [1,2,3,4,5,6,7,8,9,10,11,12]
            for i in range(0, 11):
                sheet[monthToCol(monthNums[i],"last")].value = sheet[monthToCol(monthNums[i],"this")].value
            sheet["W9"].value = monthTotal
        else:
            sheet[monthToCol(dt.today().month,"this")].value = monthTotal 



    workbook.save("excel/StockLevels_TEST.xlsx")