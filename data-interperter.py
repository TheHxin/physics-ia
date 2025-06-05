import xlsxwriter
import json
import os

workbook = xlsxwriter.Workbook("data.xlsx")
worksheet = workbook.add_worksheet()

files_raw = os.listdir("./data")
files = []

for i in files_raw:
    if i.split("-")[0] == "run":
        files.append(i)

c = 0
for i in files:
    treatment =  eval(i.split("-")[1][0])
    with open(f"./data/{i}","r") as file:
        data_raw = json.load(file)
    data_raw = list(data_raw)
    timestart = data_raw[0]["start time"]
    timeend = data_raw[1]["end time"]
    worksheet.write(1,c,f"start: {timestart} end: {timeend} delta: {timeend-timestart}")
    c = c + 5




