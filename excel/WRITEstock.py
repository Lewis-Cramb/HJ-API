import openpyxl as xlsx
import sys
sys.path.append("../HJ-API")
from general.xlsxRows import reorderList

def reorder(quantities):
    workbook = xlsx.load_workbook("excel/StockLevels.xlsx")
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



    workbook.save("excel/StockLevels.xlsx")
