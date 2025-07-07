from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel
from typing import Dict
import os
import json

class LoanEligibilityInput(BaseModel):
    financial_data: Dict  # must be provided from MCP snapshot
    loan_amount: float = 5000000  # ₹50L default
    interest_rate: float = 8.0
    tenure_years: int = 20

class LoanEligibilityOutput(BaseModel):
    result: str

def calculate_emi(principal, rate, years):
    monthly_rate = rate / (12 * 100)
    months = years * 12
    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
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
                # No snapshot data available
                msg = "❌ Financial data snapshot not found. Please fetch your data via Fi MCP first."
                return LoanEligibilityOutput(result=msg)

            # Extract financial fields
            income = data.get("income", {})
            liabilities = data.get("liabilities", {})
            monthly_salary = income.get("monthly_salary", 0)

            if monthly_salary == 0:
                result = "❌ Monthly salary not found in financial data."
                return LoanEligibilityOutput(result=result)

            # Calculate EMIs
            max_affordable_emi = monthly_salary * 0.35
            emi = calculate_emi(input.loan_amount, input.interest_rate, input.tenure_years)

            # Sum existing EMIs from liabilities
            existing_emi = 0
            for amount in liabilities.values():
                existing_emi += calculate_emi(amount, input.interest_rate, input.tenure_years)

            total_emi = existing_emi + emi

            # Determine eligibility
            if total_emi > max_affordable_emi:
                result = (
                    f"⚠️ You may not be eligible for a ₹{input.loan_amount:,.0f} loan.\n"
                    f"- Requested EMI: ₹{emi:,.0f}\n"
                    f"- Existing EMIs: ₹{existing_emi:,.0f}\n"
                    f"- Affordable limit: ₹{max_affordable_emi:,.0f}\n"
                    "💡 Consider reducing the loan amount or increasing tenure."
                )
            else:
                result = (
                    f"✅ You are eligible for a ₹{input.loan_amount:,.0f} loan.\n"
                    f"- Requested EMI: ₹{emi:,.0f}\n"
                    f"- Existing EMIs: ₹{existing_emi:,.0f}\n"
                    f"- Affordable limit: ₹{max_affordable_emi:,.0f}"
                )

            return LoanEligibilityOutput(result=result)

        except Exception as e:
            return LoanEligibilityOutput(result=f"❌ Error evaluating loan eligibility: {str(e)}")

    def default_input(self, context: ToolContext) -> LoanEligibilityInput:
        # Always require real MCP snapshot; no mocks
        snapshot_path = os.getenv("MCP_SNAPSHOT_PATH", "mcp_snapshot.json")
        if not os.path.exists(snapshot_path):
            raise FileNotFoundError("MCP snapshot file not found. Please run the Fi MCP fetch tool first.")

        with open(snapshot_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return LoanEligibilityInput(
            financial_data=data,
            loan_amount=5000000,
            interest_rate=8.0,
            tenure_years=20
        )
from langchain_core.tools import tool
import re

from .mcp_loader import load_mcp_snapshot

@tool
def check_loan_eligibility(_: str = "") -> str:
    """
    Checks if a user is eligible for a loan based on their financial data in mcp_snapshot.json.
    """
    data = load_mcp_snapshot()
    if data is None:
        return "❌ The 'mcp_snapshot.json' file is missing."
    income = data.get("income", {})
    credit_score = data.get("credit_score", 750)
    annual_income = income.get("monthly_salary", 0) * 12

    if annual_income == 0:
        return "❌ Annual income not found in your financial data."
    if credit_score < 600:
        return "Loan application is likely to be rejected due to a low credit score."
    elif 600 <= credit_score < 700:
        max_loan = annual_income * 2
        return f"You are likely eligible for a loan up to approximately ₹{max_loan:,.0f}."
    elif 700 <= credit_score < 800:
        max_loan = annual_income * 4
        return f"You have a good chance of being approved for a loan up to approximately ₹{max_loan:,.0f}."
    else:
        max_loan = annual_income * 6
        return f"With your excellent credit score, you are eligible for a premium loan up to approximately ₹{max_loan:,.0f}."