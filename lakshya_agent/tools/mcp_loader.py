import json
import os

def load_mcp_snapshot():
    file_path = os.path.join("lakshya_agent", "mcp_snapshot.json")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None