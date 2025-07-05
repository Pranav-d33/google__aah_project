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
