from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
from typing import List, Optional
from tools.memory_utils import store_tool_output

# Define the input model
class SIPPerformanceInput(BaseModel):
    financial_data: dict

# Define the output model
class SIPPerformanceOutput(BaseModel):
    summary: str

class SIPPerformanceTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="sip_performance",
            description="Analyzes SIPs in user's financial data and identifies underperforming funds."
        )

    def __call__(self, input: SIPPerformanceInput, context: ToolContext) -> SIPPerformanceOutput:
        try:
            mutual_funds = input.financial_data.get("assets", {}).get("mutual_funds", [])

            if not mutual_funds:
                return SIPPerformanceOutput(summary="🔍 No SIPs (mutual funds) found in user data.")

            underperformers = [
                fund for fund in mutual_funds if fund.get("returns", 0) < 8
            ]

            if not underperformers:
                return SIPPerformanceOutput(summary="✅ All SIPs are performing well (≥ 8% returns).")

            output_lines = ["⚠️ The following SIPs are underperforming (< 8%):"]
            for fund in underperformers:
                output_lines.append(
                    f"- {fund['name']} → ₹{fund['current_value']:,} at {fund['returns']}% returns"
                )

                summary = "\n".join(output_lines)
            store_tool_output(
                context,
                "sip_performance",
                summary,
                metadata={"underperforming": len(underperformers)}
            )
            return SIPPerformanceOutput(summary=summary)

        except Exception as e:
            return SIPPerformanceOutput(summary=f"❌ Error analyzing SIPs: {str(e)}")
from langchain_core.tools import tool
from typing import Union

from langchain_core.tools import tool
import re
import json

from .mcp_loader import load_mcp_snapshot

@tool
def get_sip_performance(_: str = "") -> str:
    """
    Calculates SIP performance using data from mcp_snapshot.json.
    """
    data = load_mcp_snapshot()
    if data is None:
        return "❌ The 'mcp_snapshot.json' file is missing."
    sips = data.get("contributions", {}).get("monthly_sip", {})
    mutual_funds = data.get("assets", {}).get("mutual_funds", [])
    if not sips or not mutual_funds:
        return "No SIP data found in your financial snapshot."
    results = []
    for mf in mutual_funds:
        name = mf["name"]
        monthly = sips.get(name, 0)
        years = 5
        rate = mf.get("returns", 10)
        i = (rate / 100) / 12
        n = years * 12
        future_value = monthly * (((1 + i)**n - 1) / i) * (1 + i)
        results.append(f"{name}: Invested ₹{monthly*n:,}, Value after {years} years: ₹{future_value:,.0f} (at {rate}% p.a.)")
    return "\n".join(results)