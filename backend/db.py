import json
import os

TABLE: dict[int, str] = {}

# Path to data.json in the same folder as this file
PATH = os.path.dirname(__file__) + "/data.json"

# not sure if this is required
def init():
    if not os.path.exists(PATH):
        with open(PATH, 'w') as f:
            f.write("{}")

def item_not_found_handler(id):
    raise ValueError(f"Item with id {id} not found")

def load():
    global TABLE
    with open(PATH, 'r') as f:
        TABLE = json.load(f)

def save():
    with open(PATH, 'w') as f:
        json.dump(TABLE, f, indent=4)

def create(name: str) -> int:
    id = len(TABLE) + 1
    TABLE[id] = name
    save()
    return id

def update(id: int, name: str):
    if id in TABLE:
        TABLE[id] = name
        save()
    else:
        item_not_found_handler(id)


def delete(id: int):
    if id in TABLE:
        del TABLE[id]
        save()
    else:
        item_not_found_handler(id)

def read(id: int) -> str:
    if id in TABLE:
        return TABLE[id]
    else:
        item_not_found_handler(id)

