from typing import List, Tuple


def model(init_request: str) -> Tuple[bool, List[str]]:
    text = init_request.strip()
    if not text:
        return False, []
    return True, [
        f"Plan work for: {text}",
        "List needed resources",
        "Execute the task",
    ]


