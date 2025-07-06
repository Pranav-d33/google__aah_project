import json

def load_mcp_snapshot():
    file_path = r"C:\Users\Admin\Project\google_aah_project\mcp_snapshot.json"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None