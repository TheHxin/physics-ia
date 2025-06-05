import asyncio
from datetime import datetime
import serial
import json
import os 

baud = 9600
port = "/dev/ttyUSB0"
root_path = __file__.rsplit("/",1)[0] + "/data"


run_name = input("Please enter new run name: ")
with open(os.path.join(root_path,run_name+".json"),"w") as file:
    json.dump([{"start time" : datetime.now().strftime("%H:%M:%S")},{"end time" : ""}],file)

from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Start Time:", current_time)

async def readSerial():
    ser = serial.Serial(port = "/dev/ttyUSB0", baudrate=9600,timeout=1)
    while True:
        await asyncio.sleep(0.2)
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if line: 
            avg = 0
            temps = line.split(",")
            for temp in temps:
                avg = avg + eval(temp)
            avg = avg / 3
            avg = round(avg, 2)

            with open(os.path.join(root_path,run_name+".json"),"r") as file:
                data = json.load(file)
            data = list(data)
            data.append({"t1" : temps[0], "t2" : temps[1], "t3" : temps[2], "avg" : str(avg)})
            print({"t1" : temps[0], "t2" : temps[1], "t3" : temps[2], "avg" : str(avg)})
            with open(os.path.join(root_path,run_name+".json"),"w") as file:
                json.dump(data,file,indent=2)


            #{"t1" : temps[0], "t2" : temps[1], "t3" : temps[2], "avg" : str(avg)}



try:
    asyncio.run(readSerial())
finally:
    with open(os.path.join(root_path,run_name+".json"),"r") as file:
        data = json.load(file)
    data = list(data)
    data[1]["end time"] = datetime.now().strftime("%H:%M:%S")
    print("End Time: " , datetime.now().strftime("%H:%M:%S"))
    with open(os.path.join(root_path,run_name+".json"),"w") as file:
        json.dump(data,file,indent=2)