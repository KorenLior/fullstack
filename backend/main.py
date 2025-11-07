import asyncio
from typing import Set, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from db import init, create, read, update, delete, get_counter, get_all_counters

app = FastAPI(
    title="Fullstack API",
    description="A FastAPI backend for the fullstack application",
    version="1.0.0"
)

init()
# Configure CORS to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI backend!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/items")
# return str or None
async def get_items(id: int):
    broadcast_table_nowait()
    return read(id)


@app.post("/api/items")
async def create_item(item: str):
    id = create(item)
    broadcast_table_nowait()
    return {"message": "Item created", "item": item, "id": id}

@app.put("/api/items")
async def update_item(id: int, item: str):
    update(id, item)
    broadcast_table_nowait()
    return {"message": "Item updated", "item": item, "id": id}

@app.delete("/api/items")
async def delete_item(id: int):
    delete(id)
    broadcast_table_nowait()
    return {"message": "Item deleted", "id": id}



clients: Set[WebSocket] = set()

@app.websocket("/ws_counters")
async def ws(ws: WebSocket):
    await ws.accept()
    clients.add(ws)
    try:
        await ws.send_json(get_all_counters())  # initial state
        while True:
            await ws.receive_text()  # keep alive, ignore input
    except WebSocketDisconnect:
        clients.discard(ws)

async def _broadcast(snapshot: Dict[int, int]):
    for c in list(clients):
        try:
            await c.send_json(snapshot)
        except Exception:
            clients.discard(c)

def broadcast_table_nowait():
    """Call after you mutate `table`. Returns immediately."""
    asyncio.get_running_loop().create_task(_broadcast(get_all_counters()))