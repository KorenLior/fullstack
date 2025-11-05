from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init, load, create, read, update, delete

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
    return read(id)


@app.post("/api/items")
async def create_item(item: str):
    id = create(item)
    return {"message": "Item created", "item": item, "id": id}

@app.put("/api/items")
async def update_item(id: int, item: str):
    update(id, item)
    return {"message": "Item updated", "item": item, "id": id}

@app.delete("/api/items")
async def delete_item(id: int):
    delete(id)
    return {"message": "Item deleted", "id": id}

