import json
import os
from typing import Any, Dict

Item = Dict[str, Any]

TABLE: dict[int, Item] = {}
COUNTER: dict[int, int] = {}  # Counter for each item

# Path to data.json in the same folder as this file
PATH = "C:/Users/tamir/OneDrive/Desktop/fullstack/backend/data.json"
COUNTER_PATH = "C:/Users/tamir/OneDrive/Desktop/fullstack/backend/counter.json"


def init() -> None:
    if not os.path.exists(PATH):
        with open(PATH, "w") as f:
            f.write("{}")
    if not os.path.exists(COUNTER_PATH):
        with open(COUNTER_PATH, "w") as f:
            f.write("{}")


def item_not_found_handler(id: int) -> None:
    raise ValueError(f"Item with id {id} not found")


def save() -> None:
    serialized_table = {str(k): _serialize_item(v) for k, v in TABLE.items()}
    serialized_counter = {str(k): v for k, v in COUNTER.items()}
    with open(PATH, "w") as f:
        json.dump(serialized_table, f, indent=4)
    with open(COUNTER_PATH, "w") as f:
        json.dump(serialized_counter, f, indent=4)


def create(init_request: str) -> int:
    new_id = max(TABLE.keys(), default=0) + 1
    TABLE[new_id] = _make_item(init_request)
    COUNTER[new_id] = 0  # Initialize counter to 0
    save()
    return new_id


def update(id: int, init_request: str) -> None:
    if id in TABLE:
        TABLE[id]["init_request"] = init_request
        COUNTER[id] = COUNTER.get(id, 0) + 1  # Increment counter
        save()
    else:
        item_not_found_handler(id)


def delete(id: int) -> None:
    if id in TABLE:
        del TABLE[id]
        assert id in COUNTER, f"Counter for item {id} not found"
        del COUNTER[id]
        save()
    else:
        item_not_found_handler(id)


def read(id: int) -> Item:
    if id in TABLE:
        assert id in COUNTER, f"Counter for item {id} not found"
        COUNTER[id] = COUNTER.get(id, 0) + 1  # Increment counter
        save()
        return _serialize_item(TABLE[id])
    else:
        item_not_found_handler(id)


def get_table() -> dict[int, Item]:
    return {k: _serialize_item(v) for k, v in TABLE.items()}


def get_counter(id: int) -> int:
    assert id in COUNTER, f"Counter for item {id} not found"
    return COUNTER.get(id, 0)


def get_all_counters() -> dict[int, int]:
    return COUNTER


def _make_item(init_request: str) -> Item:
    return {"init_request": init_request, "action_tasks": []}


def _serialize_item(item: Item) -> Item:
    init_request = item.get("init_request") or item.get("value", "")
    actions = item.get("action_tasks", [])
    return {
        "init_request": str(init_request),
        "action_tasks": [str(action) for action in actions],
    }
