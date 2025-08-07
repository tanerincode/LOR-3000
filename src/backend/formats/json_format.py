import json


def format_json(content: str) -> str:
    return json.dumps({"content": content})
