import json
import os
from pathlib import Path
from typing import List, Optional, Tuple

from openai import OpenAI

MODEL_NAME = os.getenv("FLOWPAD_MODEL", "gpt-4o-mini")
ENV_VAR_NAME = "FLOWPAD_OPENAI_API_KEY"
SECRET_FILE = Path(__file__).with_name("openai_api_key.txt")


def _load_api_key() -> Optional[str]:
    """Return the OpenAI API key from env var or local secret file."""
    api_key = os.getenv(ENV_VAR_NAME)
    if api_key:
        return api_key.strip()

    if SECRET_FILE.exists():
        try:
            return SECRET_FILE.read_text(encoding="utf-8").strip()
        except OSError:
            return None

    return None


def model(init_request: str) -> Tuple[bool, List[str]]:
    text = init_request.strip()
    if not text:
        return False, []
    api_key = _load_api_key()
    if not api_key:
        return False, []
    client = OpenAI(api_key=api_key)
    prompt = (
        'Respond with JSON: {"valid": bool, "actions": [strings]}. '
        "Only mark valid when the request is actionable. "
        "Be concise and to the point. "
        "actions should be a list of strings, each an actionable task to complete the overall task. "
        "the list should be no more than 5 actions, and no fewer than 2. "
        f"Task: {text}"
    )
    print("Prompt:", prompt)
    try:
        reply = client.responses.create(model=MODEL_NAME, input=prompt, temperature=0.2)
        content = reply.output[0].content[0].text
        print("OpenAI content:", content)
        data = json.loads(content)
        return bool(data.get("valid")), [str(step) for step in data.get("actions", [])]
    except Exception as exc:
        print("OpenAI error:", exc)
        return False, []

