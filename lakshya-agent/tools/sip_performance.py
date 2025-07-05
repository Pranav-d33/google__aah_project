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
