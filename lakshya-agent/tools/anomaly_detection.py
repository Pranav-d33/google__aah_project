from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
from typing import Dict, List

from tools.memory_utils import store_tool_output

class AnomalyDetectionInput(BaseModel):
    financial_data: Dict

class AnomalyDetectionOutput(BaseModel):
    anomalies: str

class AnomalyDetectionTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="anomaly_detection",
            description="Detects unusual financial changes like sudden dips, negative returns, or credit score drops."
        )

    def __call__(self, input: AnomalyDetectionInput, context: ToolContext) -> AnomalyDetectionOutput:
       try:
        data = input.financial_data
        anomalies = []

        # Check for low bank balance
        bank_balance = data.get("assets", {}).get("bank_balance", 0)
        if bank_balance < 10000:
            anomalies.append(f"⚠️ Bank balance is quite low: ₹{bank_balance:,}")

        # Check for negative returns in mutual funds
        mutual_funds = data.get("assets", {}).get("mutual_funds", [])
        for fund in mutual_funds:
            if fund.get("returns", 0) < 0:
                anomalies.append(f"🔻 Negative return in SIP: {fund['name']} → {fund['returns']}%")

        # Check for credit score drop
        credit_score = data.get("credit_score", 0)
        if credit_score and credit_score < 650:
            anomalies.append(f"⚠️ Low credit score detected: {credit_score}")

        # Check for high liabilities
        liabilities = data.get("liabilities", {})
        total_liabilities = sum(liabilities.values())
        if total_liabilities > 1000000:
            anomalies.append(f"💸 High total liabilities: ₹{total_liabilities:,}")

        # Handle the results
        if not anomalies:
            summary = "✅ No major anomalies detected."
            store_tool_output(
             context,
                "anomaly_detection", 
                summary,
                metadata={"count": 0}
            )
            return AnomalyDetectionOutput(anomalies=summary)

        # If anomalies were found
        summary = "\n".join(anomalies)
        store_tool_output(
            context,
            "anomaly_detection",
            summary,
            metadata={"count": len(anomalies)}
        )
        return AnomalyDetectionOutput(anomalies=summary)

       except Exception as e:
        return AnomalyDetectionOutput(anomalies=f"❌ Error in anomaly detection: {str(e)}")
       
from langchain_core.tools import tool
from typing import List
import json
from .mcp_loader import load_mcp_snapshot
import numpy as np

@tool
def detect_anomaly(_: str = "") -> str:
    """
    Detects anomalies in expenses using data from mcp_snapshot.json.
    """
    data = load_mcp_snapshot()
    if data is None:
        return "❌ The 'mcp_snapshot.json' file is missing."
    expenses = [m["expenses"] for m in data.get("expense_history", [])]
    if not expenses:
        return "No expense history found."
    mean = np.mean(expenses)
    std = np.std(expenses)
    threshold = mean + 2 * std
    anomalies = [e for e in expenses if e > threshold]
    if anomalies:
        return f"Anomalies detected: {anomalies}. Mean: {mean:.2f}, Threshold: {threshold:.2f}"
    else:
        return "No anomalies detected in your expenses."