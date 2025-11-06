import json
import os

TABLE: dict[int, str] = {}
COUNTER: dict[int, int] = {}  # Counter for each item

# Path to data.json in the same folder as this file
PATH = "C:/Users/tamir/OneDrive/Desktop/fullstack/backend/data.json"
COUNTER_PATH = "C:/Users/tamir/OneDrive/Desktop/fullstack/backend/counter.json"

# not sure if this is required
def init():
    if not os.path.exists(PATH):
        with open(PATH, 'w') as f:
            f.write("{}")
    if not os.path.exists(COUNTER_PATH):
        with open(COUNTER_PATH, 'w') as f:
            f.write("{}")

def item_not_found_handler(id):
    raise ValueError(f"Item with id {id} not found")

def load():
    global TABLE, COUNTER
    with open(PATH, 'r') as f:
        TABLE = json.load(f)
    with open(COUNTER_PATH, 'r') as f:
        COUNTER = json.load(f)

def save():
    with open(PATH, 'w') as f:
        json.dump(TABLE, f, indent=4)
    with open(COUNTER_PATH, 'w') as f:
        json.dump(COUNTER, f, indent=4)

def create(name: str) -> int:
    id = len(TABLE) + 1
    TABLE[id] = name
    COUNTER[id] = 0  # Initialize counter to 0
    save()
    return id

def update(id: int, name: str):
    if id in TABLE:
        TABLE[id] = name
        COUNTER[id] = COUNTER.get(id, 0) + 1  # Increment counter
        save()
    else:
        item_not_found_handler(id)


def delete(id: int):
    if id in TABLE:
        del TABLE[id]
        assert id in COUNTER, f"Counter for item {id} not found"
        del COUNTER[id]
        save()
    else:
        item_not_found_handler(id)

def read(id: int) -> str:
    if id in TABLE:
        assert id in COUNTER, f"Counter for item {id} not found"
        COUNTER[id] = COUNTER.get(id, 0) + 1  # Increment counter
        save()
        return TABLE[id]
    else:
        item_not_found_handler(id)

def get_table() -> dict[int, str]:
    return TABLE


def get_counter(id: int) -> int:
    assert id in COUNTER, f"Counter for item {id} not found"
    return COUNTER.get(id, 0)

def get_all_counters():
    return COUNTER
    

