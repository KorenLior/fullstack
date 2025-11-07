from typing import List


def model(init_request: str) -> List[str]:
    return [f"suggestion: {init_request}", "follow-up: check dependencies","task: do this3"]

