from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()
connected_clients = []

baud = 9600
port = "/dev/ttyUSB0"
root_path = __file__.rsplit("/",1)[0]

@app.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Real-time Counter</title></head>
    <body>
        <h1>Temperature One: <span id="t1">0</span></h1>
        <h1>Temperature Two: <span id="t2">0</span></h1>
        <h1>Temperature Three: <span id="t3">0</span></h1>
        <h1>Avrage: <span id="avg">0</span></h1>
        <script>
            let ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                let data = JSON.parse(event.data);

                document.getElementById("t1").innerText = data.t1;
                document.getElementById("t2").innerText = data.t2;
                document.getElementById("t3").innerText = data.t3;
                document.getElementById("avg").innerText = data.avg;
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        pass
    finally:
        connected_clients.remove(websocket)
