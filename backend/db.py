import json
from pathlib import Path

from mock_model import model
# from model import model
from task import Task

TABLE: dict[int, Task] = {}
COUNTER: dict[int, int] = {}  # Counter for each item

BASE_DIR = Path(__file__).resolve().parent
PATH = BASE_DIR / "data.json"
COUNTER_PATH = BASE_DIR / "counter.json"


def init() -> None:
    if not PATH.exists():
        PATH.write_text("{}")
    if not COUNTER_PATH.exists():
        COUNTER_PATH.write_text("{}")


def item_not_found_handler(id: int) -> None:
    raise ValueError(f"Item with id {id} not found")


def save() -> None:
    serialized_table = {str(k): v.to_dict() for k, v in TABLE.items()}
    serialized_counter = {str(k): v for k, v in COUNTER.items()}
    with open(PATH, "w") as f:
        json.dump(serialized_table, f, indent=4)
    with open(COUNTER_PATH, "w") as f:
        json.dump(serialized_counter, f, indent=4)


def create(init_request: str) -> int:
    valid, actions = model(init_request=init_request)
    if not valid:
        raise ValueError("Init request is not a valid task")
    new_id = max(TABLE.keys(), default=0) + 1
    TABLE[new_id] = Task(init_request=init_request, action_tasks=list(actions))
    COUNTER[new_id] = 0  # Initialize counter to 0
    save()
    return new_id


def update(id: int, init_request: str) -> None:
    if id in TABLE:
        valid, actions = model(init_request=init_request)
        if not valid:
            raise ValueError("Init request is not a valid task")
        task = TABLE[id]
        task.init_request = init_request
        task.action_tasks = list(actions)
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


def read(id: int) -> dict[str, object]:
    if id in TABLE:
        assert id in COUNTER, f"Counter for item {id} not found"
        COUNTER[id] = COUNTER.get(id, 0) + 1  # Increment counter
        save()
        return TABLE[id].to_dict()
    else:
        item_not_found_handler(id)


def get_table() -> dict[int, dict[str, object]]:
    return {k: v.to_dict() for k, v in TABLE.items()}


def get_counter(id: int) -> int:
    assert id in COUNTER, f"Counter for item {id} not found"
    return COUNTER.get(id, 0)


def get_all_counters() -> dict[int, int]:
    return COUNTER