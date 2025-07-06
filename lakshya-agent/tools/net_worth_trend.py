from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
from typing import Dict, List
import pandas as pd
#from tools.memory_utils import store_tool_output


class NetWorthTrendInput(BaseModel):
    financial_data: Dict

class NetWorthTrendOutput(BaseModel):
    trend_summary: str

class NetWorthTrendTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="net_worth_trend",
            description="Analyzes and summarizes the user's net worth growth over time."
        )

    def __call__(self, input: NetWorthTrendInput, context: ToolContext) -> NetWorthTrendOutput:
        try:
            history = input.financial_data.get("net_worth_history", [])
            if not history:
                return NetWorthTrendOutput(trend_summary="📉 No net worth history data found.")

            df = pd.DataFrame(history)
            df['month'] = pd.to_datetime(df['month'], format="%Y-%m")
            df = df.sort_values(by='month')
            df['value'] = df['value'].astype(float)

            start_value = df.iloc[0]['value']
            end_value = df.iloc[-1]['value']
            change = end_value - start_value
            pct_change = (change / start_value) * 100 if start_value != 0 else 0

            summary = (
                f"📊 Net Worth Trend ({df.iloc[0]['month'].strftime('%b %Y')} → {df.iloc[-1]['month'].strftime('%b %Y')}):\n"
                f"- Start: ₹{start_value:,.0f}\n"
                f"- End: ₹{end_value:,.0f}\n"
                f"- Change: ₹{change:,.0f} ({pct_change:.2f}%)\n"
            )

            if pct_change >= 20:
                summary += "✅ Strong upward trend in your net worth. Keep it up!"
            elif pct_change >= 0:
                summary += "🟡 Mild growth in net worth. Explore ways to accelerate."
            else:
                summary += "🔴 Decline in net worth. Review your expenses/investments."

            return NetWorthTrendOutput(trend_summary=summary)

        except Exception as e:
            return NetWorthTrendOutput(trend_summary=f"❌ Error analyzing net worth trend: {str(e)}")
from langchain_core.tools import tool
import json

from .mcp_loader import load_mcp_snapshot

@tool
def get_net_worth_trend(_: str = "") -> str:
    """
    Summarizes net worth trend using data from mcp_snapshot.json.
    """
    data = load_mcp_snapshot()
    if data is None:
        return "❌ The 'mcp_snapshot.json' file is missing."
    history = data.get("net_worth_history", [])
    if not history:
        return "No net worth history found."
    start = history[0]
    end = history[-1]
    change = end["value"] - start["value"]
    pct = (change / start["value"]) * 100 if start["value"] else 0
    return (f"Net worth grew from ₹{start['value']:,} to ₹{end['value']:,} "
            f"({pct:.2f}% change) between {start['month']} and {end['month']}.")