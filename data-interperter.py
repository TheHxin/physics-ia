import xlsxwriter
from datetime import datetime
import json
import os

workbook = xlsxwriter.Workbook("data.xlsx")
worksheet = workbook.add_worksheet()

files_raw = os.listdir("./data")
files = []

for i in files_raw:
    if i.split("-")[0] == "run":
        files.append(i)
files.sort()
treatment_c = 0
for i in files:
    with open(f"./data/{i}","r") as file:
        data_raw = json.load(file)
    data_raw = list(data_raw)
    i = i.split(".")[0]
    treatment =  i.split("-",1)[1]
    timestart = data_raw[0]["start time"]
    timeend = data_raw[1]["end time"]
    delta_temp = eval(data_raw[len(data_raw)-1]["avg"])-eval(data_raw[2]["avg"])
    delta_temp = round(delta_temp,2)
    
    for j in range(2):
        data_raw.pop(0)

    worksheet.write(0,treatment_c,f"{treatment} ")
    worksheet.write(1,treatment_c,f"{datetime.strptime(timeend , '%H:%M:%S')-datetime.strptime(timestart,'%H:%M:%S')}")
    worksheet.write(2,treatment_c,f"DT: {delta_temp}")
    
    
    
    for temp_c in range(3,len(data_raw)):
        worksheet.write(temp_c,treatment_c,data_raw[temp_c]["avg"])
    

    treatment_c = treatment_c + 1

workbook.close()




