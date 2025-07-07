from pydantic import BaseModel
from typing import Dict, List, Optional
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from .mcp_loader import load_mcp_snapshot

class FinancialPlannerInput(BaseModel):
    financial_data: Dict

class RetirementScenario(BaseModel):
    scenario: str
    projected_amount: float

class TaxOptimizationRecommendation(BaseModel):
    recommendation: str

class FinancialPlannerOutput(BaseModel):
    money_at_40: float
    retirement_simulations: List[RetirementScenario]
    tax_optimization: TaxOptimizationRecommendation

def calculate_future_value(present_value: float, annual_rate: float, years: int) -> float:
    return present_value * ((1 + annual_rate) ** years)

class AdvancedFinancialPlannerTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="advanced_financial_planner",
            description="Computes financial planning simulations and tax optimization based on snapshot data"
        )

    def __call__(self, input: FinancialPlannerInput, context: ToolContext) -> FinancialPlannerOutput:
        data = input.financial_data
        user_profile = data.get("user_profile", {})
        income = data.get("income", {})
        contributions = data.get("contributions", {})
        tax_info = data.get("tax_info", {})
        projection = data.get("projection_assumptions", {})

        age = user_profile.get("age", 21)
        retirement_age = user_profile.get("retirement_age", 60)
        years_to_40 = max(40 - age, 0)

        monthly_salary = income.get("monthly_salary", 0)
        monthly_savings = contributions.get("monthly_savings", 0)
        roi = projection.get("equity_return_percent", 10) / 100
        inflation = projection.get("inflation_rate_percent", 5) / 100

        # Calculate money at 40 assuming monthly savings grow at ROI minus inflation
        total_amount = 0.0
        for year in range(years_to_40):
            total_amount = (total_amount + monthly_savings * 12) * (1 + roi - inflation)

        # Retirement planning simulations
        scenarios = []
        for scenario_name, roi_pct in [("Conservative", 0.04), ("Moderate", 0.06), ("Aggressive", 0.08)]:
            years_to_retirement = max(retirement_age - age, 0)
            projected = calculate_future_value(total_amount, roi_pct, years_to_retirement)
            scenarios.append(RetirementScenario(scenario=scenario_name, projected_amount=round(projected, 2)))

        # Tax optimization recommendations
        deductions = tax_info.get("deductions", {})
        limit_80C = deductions.get("80C_limit", 150000)
        utilized_80C = deductions.get("80C_utilized", 0)
        remaining_80C = max(limit_80C - utilized_80C, 0)

        if remaining_80C > 0:
            tax_recommendation = f"Consider investing ₹{remaining_80C} more under section 80C to optimize tax savings."
        else:
            tax_recommendation = "You have fully utilized your 80C deductions. Consider other tax saving instruments."

        tax_opt = TaxOptimizationRecommendation(recommendation=tax_recommendation)

        return FinancialPlannerOutput(
            money_at_40=round(total_amount, 2),
            retirement_simulations=scenarios,
            tax_optimization=tax_opt
        )

    def default_input(self, context: ToolContext) -> FinancialPlannerInput:
        data = load_mcp_snapshot()
        if data is None:
            raise FileNotFoundError("mcp_snapshot.json not found.")
        return FinancialPlannerInput(financial_data=data)
