import json


def json_formatter(input: str) -> str:
    data = json.loads(input)
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"
