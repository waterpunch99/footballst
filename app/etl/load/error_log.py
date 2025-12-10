import json
from datetime import datetime

def log_load_error(table_name: str, error: Exception, payload=None):
  
    record = {
        "table": table_name,
        "error": str(error),
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat(),
    }

    with open("load_errors.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
