from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
import json
import os

from tools.memory_utils import store_tool_output

class FetchFinancialDataInput(BaseModel):
    pass

class FetchFinancialDataOutput(BaseModel):
    financial_data: dict

class FetchFinancialDataTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="fetch_financial_data",
            description="Fetches the user's structured financial data from Fi MCP or local mock file."
        )

    def __call__(self, input: FetchFinancialDataInput, context: ToolContext) -> FetchFinancialDataOutput:
        try:
            # Reads snapshot saved by your MCP connector or dev tool
            snapshot_path = os.getenv("MCP_SNAPSHOT_PATH", "mcp_snapshot.json")

            if not os.path.exists(snapshot_path):
                return FetchFinancialDataOutput(financial_data={})

            with open(snapshot_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                store_tool_output(
    context,
    "fetch_financial_data",
    "Fetched financial snapshot successfully.",
    metadata={"keys": list(data.keys())}
)


            return FetchFinancialDataOutput(financial_data=data)

        except Exception as e:
            return FetchFinancialDataOutput(financial_data={"error": str(e)})
        
from langchain_core.tools import tool

import json
from .mcp_loader import load_mcp_snapshot

@tool
def fetch_financial_data(_: str = "") -> str:
    """
    Fetches all financial data from mcp_snapshot.json.
    """
    data = load_mcp_snapshot()
    if data is None:
        return "❌ The 'mcp_snapshot.json' file is missing."
    return f"Financial snapshot loaded. Top-level keys: {', '.join(data.keys())}"
