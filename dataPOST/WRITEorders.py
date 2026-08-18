import openpyxl as xlsx
from datetime import date as dt


def upload(orders):
    sheetNum = 1
    workbook = xlsx.load_workbook("dataPOST/D2c Stock and Sales Sheet.xlsx")
    sheets = workbook.sheetnames
    sheetName = sheets[sheetNum]
    sheet = workbook[sheetName]

    lines = []

    for order in orders:
        info = {"Date":"","SKU":"","Product":"","Order/Reference":"","Movement Type":"Sale / Order","Quantity":""}
        info["Date"] = dt.fromisoformat(order["orderDate"]).strftime("%d/%m/%Y")
        info["Order/Reference"] = order["custPO"]
        for product in order["products"]:
            info["Product"] = product
            info["Quantity"] = order["products"][product][0]
            info["SKU"] = order["products"][product][1]

            lines.append(info)

    row = 0
    for i, cell in enumerate(sheet["A"]):
        pass

    row = i+2

    merged_range = list(sheet.merged_cells.ranges)
    for merged_cell_range in merged_range:
        sheet.unmerge_cells(str(merged_cell_range))

    for line in lines:
        sheet[f"A{row}"] = line["Date"]
        sheet[f"B{row}"] = line["SKU"]
        sheet[f"C{row}"] = line["Product"]
        sheet[f"D{row}"] = line["Order/Reference"]
        sheet[f"E{row}"] = line["Movement Type"]
        sheet[f"F{row}"] = line["Quantity"]
        row += 1

    workbook.save("dataPOST/D2c Stock and Sales Sheet.xlsx")
    print()