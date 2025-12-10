import json
from datetime import datetime

def save_dead_letter(table_name: str, record: dict, reason: str):

    output = {
        "table": table_name,
        "record": record,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
    }

    with open("dead_letter.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(output, ensure_ascii=False) + "\n")
