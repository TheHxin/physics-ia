from webserver import connected_clients
import subprocess
import threading
import uvicorn
import asyncio
import serial
import json
import os


baud = 9600
port = "/dev/ttyUSB0"
root_path = __file__.rsplit("/",1)[0]

current_run_name : str = ""
current_run : asyncio.Task = None

def startUvicorn():
    uvicorn.run("webserver:app", host="localhost", port=8000, access_log=False, log_level="critical")

# Background task to simulate changing the integer value
async def readSerial():
    ser = serial.Serial(port = "/dev/ttyUSB0",baud = 9600,timeout=1)
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

            dumpData({"t1" : temps[0], "t2" : temps[1], "t3" : temps[2], "avg" : str(avg)})
#            for ws in connected_clients:
#                try:
#                    pass
#                    await ws.send_json({"t1" : temps[0],
#                                        "t2" : temps[1],
#                                        "t3" : temps[2],
#                                        "avg" : str(avg)})
#                except:
#                    pass

async def dumpData(data: dict):
    asyncio.create_task(dumpDataWebSocket(data))
    asyncio.create_task(dumpDataFile(data=data))



async def dumpDataWebSocket(data : dict):
    for ws in connected_clients:
        ws.send_json(data)

async def dumpDataFile(data : dict, path = os.path.join(__file__.rsplit("/",1)[0],"/data")):
    try:
        with open(os.path.join(path,current_run_name), "r") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        with open(os.path.join(path,current_run_name), "w") as file:
            json.dump("[]",file,indent=2)
            json_data = []

    json_data = list(json_data)
    json_data.append(data)

    with open(os.path.join(path,current_run_name), "w") as file:
        json.dump(json_data,file,indent=2)






async def Main():
    #await asyncio.create_subprocess_shell("uvicorn webserver:app")
    webserver = threading.Thread(target=startUvicorn)
    webserver.start()
    await asyncio.sleep(2)
    print("Webserver Started ...")

    while True:
        global current_run_name
        global current_run

        current_run_name = input("Enter the new run name: ")
        current_run = asyncio.create_task(readSerial())

        if input("Enter 1 to exit: ") == "1":
            current_run.cancel()

    
asyncio.run(Main())