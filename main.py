import asyncio
import psutil
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from llama_cpp import Llama

logging.basicConfig(
    filename="ai_core.log", 
    level=logging.INFO, 
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)

app = FastAPI()

logging.info("Init model Qwen 2.5 14B...")
llm = Llama(
    model_path="./Qwen2.5-14B-Instruct-Q5_K_M.gguf",
    n_ctx=8192,
    n_threads=12,
    verbose=False
)
llm_lock = asyncio.Lock()
logging.info("Succsesful loading in RAM.")

# --- Monitoring hardware ---
def get_hardware_stats():
    stats = {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_used": round(psutil.virtual_memory().used / (1024**3), 1),
        "disk_percent": psutil.disk_usage('/').percent,
        "temp_cpu": "N/A",
        "temp_nvme": "N/A"
    }
    
    # Temperature
    if hasattr(psutil, "sensors_temperatures"):
        sensors = psutil.sensors_temperatures()
        if "coretemp" in sensors:
            stats["temp_cpu"] = f"{sensors['coretemp'][0].current}°C"
        if "nvme" in sensors:
            stats["temp_nvme"] = f"{sensors['nvme'][0].current}°C"
            
    return stats

@app.get("/")
async def chat_page():
    with open("chat.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/admin")
async def admin_page():
    with open("admin.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/api/stats")
async def api_stats():
    return get_hardware_stats()

@app.get("/api/logs")
async def api_logs():
    try:
        with open("ai_core.log", "r", encoding="utf-8") as f:
            lines = f.readlines()[-20:]
            return {"logs": "".join(lines)}
    except FileNotFoundError:
        return {"logs": "Log-file is empty."}

@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logging.info(f"New connect: {websocket.client.host}")
    try:
        while True:
            user_message = await websocket.receive_text()
            logging.info(f"Request recieved: {user_message[:50]}...")
            
            async with llm_lock:
                await websocket.send_text("[START]")
                logging.info("Generation...")
                
                response = llm.create_chat_completion(
                    messages=[
                        {"role": "system", "content": "You usefull assistant."},
                        {"role": "user", "content": user_message}
                    ],
                    max_tokens=1024,
                    temperature=0.7,
                    stream=True
                )
                
                for chunk in response:
                    if "content" in chunk["choices"][0]["delta"]:
                        token = chunk["choices"][0]["delta"]["content"]
                        await websocket.send_text(token)
                        await asyncio.sleep(0.005)
                
                await websocket.send_text("[END]")
                logging.info("Generation complited.")
                
    except WebSocketDisconnect:
        logging.info("Client disconnected.")
