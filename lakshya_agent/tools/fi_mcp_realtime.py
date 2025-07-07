from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
from typing import Optional
import requests
import json
import os

class FiMCPRealtimeInput(BaseModel):
    api_token: str  # Provided by user

class FiMCPRealtimeOutput(BaseModel):
    status: str

class FiMCPRealtimeTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="fi_mcp_realtime_fetch",
            description="Fetches the latest snapshot from Fi MCP using API token and updates local snapshot file."
        )

    def __call__(self, input: FiMCPRealtimeInput, context: ToolContext) -> FiMCPRealtimeOutput:
        try:
            headers = {
                "Authorization": f"Bearer {input.api_token}"
            }
            url = "https://mcp.fi.money:8080/mcp/stream"

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code != 200:
                return FiMCPRealtimeOutput(status=f"❌ Failed to fetch data: HTTP {response.status_code}")

            data = response.json()

            with open("mcp_snapshot.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return FiMCPRealtimeOutput(status="✅ Live snapshot fetched and updated successfully.")

        except Exception as e:
            return FiMCPRealtimeOutput(status=f"❌ Error fetching snapshot: {str(e)}")
from langchain_core.tools import tool
import random

import json

from .mcp_loader import load_mcp_snapshot

@tool
def get_fi_mcp_realtime(_: str = "") -> str:
    """
    Returns a summary of assets from mcp_snapshot.json.
    """
    data = load_mcp_snapshot()
    if data is None:
        return "❌ The 'mcp_snapshot.json' file is missing."
    assets = data.get("assets", {})
    summary = []
    for k, v in assets.items():
        if isinstance(v, (int, float)):
            summary.append(f"{k.replace('_', ' ').title()}: ₹{v:,}")
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    name = item.get("name") or item.get("symbol") or item.get("bank") or "Unknown"
                    val = item.get("current_value") or item.get("amount") or 0
                    summary.append(f"{name}: ₹{val:,}")
    return "Your asset summary:\n" + "\n".join(summary)