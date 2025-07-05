from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
from typing import Dict
import math
import os
import json

from tools.memory_utils import store_tool_output  # ✅ helper to log to memory

class LoanEligibilityInput(BaseModel):
    financial_data: Dict = {}  # filled via fetch_financial_data tool or mock
    loan_amount: float = 5000000  # ₹50L default
    interest_rate: float = 8.0
    tenure_years: int = 20

class LoanEligibilityOutput(BaseModel):
    result: str

def calculate_emi(principal, rate, years):
    monthly_rate = rate / (12 * 100)
    months = years * 12
    emi = (principal * monthly_rate * math.pow(1 + monthly_rate, months)) / (math.pow(1 + monthly_rate, months) - 1)
    return emi

class LoanEligibilityTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="loan_eligibility",
            description="Checks loan eligibility for a given amount based on income, liabilities, interest rate, and tenure"
        )

    def __call__(self, input: LoanEligibilityInput, context: ToolContext) -> LoanEligibilityOutput:
        try:
            data = input.financial_data

            if not data:
                # 🔁 fallback to MCP snapshot if data not injected
                snapshot_path = os.getenv("MCP_SNAPSHOT_PATH", "mcp_snapshot.json")
                if os.path.exists(snapshot_path):
                    with open(snapshot_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    context.logger.info("Loaded financial data from snapshot.")
                else:
                    data = {
                        "income": {"monthly_salary": 75000},
                        "liabilities": {"car_loan": 200000},
                        "credit_score": 765,
                        "assets": {"bank_balance": 520000},
                    }
                    context.logger.warning("No MCP snapshot found. Using mock data.")

            income = data.get("income", {})
            liabilities = data.get("liabilities", {})
            monthly_salary = income.get("monthly_salary", 0)

            if monthly_salary == 0:
                result = "❌ Monthly salary not found in financial data."
                store_tool_output(
                    context,
                    tool_name="loan_eligibility",
                    summary=result,
                    metadata={"error": "no_salary_data"}
                )
                return LoanEligibilityOutput(result=result)

            max_affordable_emi = monthly_salary * 0.35
            emi = calculate_emi(input.loan_amount, input.interest_rate, input.tenure_years)

            existing_emi = 0
            for _, amount in liabilities.items():
                existing_emi += calculate_emi(amount, 8.0, 5)

            total_emi = existing_emi + emi

            if total_emi > max_affordable_emi:
                result = (
                    f"⚠️ You may not be eligible for a ₹{input.loan_amount:,.0f} loan.\n"
                    f"- Requested EMI: ₹{emi:,.0f}\n"
                    f"- Existing EMIs: ₹{existing_emi:,.0f}\n"
                    f"- Affordable limit: ₹{max_affordable_emi:,.0f}\n"
                    f"💡 Consider reducing the loan amount or increasing tenure."
                )
            else:
                result = (
                    f"✅ You are eligible for a ₹{input.loan_amount:,.0f} loan.\n"
                    f"- Requested EMI: ₹{emi:,.0f}\n"
                    f"- Existing EMIs: ₹{existing_emi:,.0f}\n"
                    f"- Affordable limit: ₹{max_affordable_emi:,.0f}"
                )

            store_tool_output(
                context,
                tool_name="loan_eligibility",
                summary=result,
                metadata={
                    "loan_amount": input.loan_amount,
                    "interest_rate": input.interest_rate,
                    "tenure_years": input.tenure_years,
                    "total_emi": total_emi,
                    "affordable": total_emi <= max_affordable_emi
                }
            )

            return LoanEligibilityOutput(result=result)

        except Exception as e:
            return LoanEligibilityOutput(result=f"❌ Error: {str(e)}")

    def default_input(self, context: ToolContext) -> LoanEligibilityInput:
        snapshot_path = os.getenv("MCP_SNAPSHOT_PATH", "mcp_snapshot.json")
        try:
            with open(snapshot_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                context.logger.info("Loaded financial data from snapshot for default_input.")
        except Exception:
            context.logger.warning("Using fallback mock data in default_input().")
            data = {
                "income": {"monthly_salary": 75000},
                "liabilities": {"home_loan": 1800000, "car_loan": 200000},
                "credit_score": 765,
                "assets": {"bank_balance": 520000},
            }

        return LoanEligibilityInput(
            financial_data=data,
            loan_amount=5000000,
            interest_rate=8.0,
            tenure_years=20
        )