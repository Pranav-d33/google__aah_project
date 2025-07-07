from pydantic import BaseModel
from typing import Dict, List, Optional
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from .mcp_loader import load_mcp_snapshot

class PortfolioRebalanceAction(BaseModel):
    asset: str
    current_weight: float
    target_weight: float
    action: str  # "Buy", "Sell", or "Hold"
    amount: Optional[float] = None

class AssetAllocationAnalysis(BaseModel):
    age: int
    risk_profile: str
    recommended_allocation: Dict[str, float]

class SIPAdjustmentSuggestion(BaseModel):
    suggestion: str

class InvestmentStrategyInput(BaseModel):
    financial_data: Dict

class InvestmentStrategyOutput(BaseModel):
    rebalance_actions: List[PortfolioRebalanceAction]
    allocation_analysis: AssetAllocationAnalysis
    sip_adjustment: SIPAdjustmentSuggestion

class InvestmentStrategyOptimizerTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="investment_strategy_optimizer",
            description="Recommends portfolio rebalancing, asset allocation analysis, and SIP timing adjustments"
        )

    def __call__(self, input: InvestmentStrategyInput, context: ToolContext) -> InvestmentStrategyOutput:
        data = input.financial_data
        user_profile = data.get("user_profile", {})
        age = user_profile.get("age", 21)
        risk_profile = user_profile.get("risk_profile", "moderate")

        assets = data.get("assets", {})
        asset_allocation = data.get("asset_allocation", {})

        # Calculate current weights from holdings
        total_value = 0.0
        current_weights = {}

        # Sum all asset values
        for key in ["bank_balance", "mutual_funds", "stocks", "epf", "fixed_deposits", "real_estate"]:
            val = assets.get(key, 0)
            if isinstance(val, list):
                total_value += sum(item.get("current_value", 0) if isinstance(item, dict) else 0 for item in val)
            elif isinstance(val, (int, float)):
                total_value += val

        # Calculate weights for each category
        def get_asset_value(key):
            val = assets.get(key, 0)
            if isinstance(val, list):
                return sum(item.get("current_value", 0) if isinstance(item, dict) else 0 for item in val)
            elif isinstance(val, (int, float)):
                return val
            return 0

        categories = ["bank_balance", "mutual_funds", "stocks", "epf", "fixed_deposits", "real_estate"]
        for cat in categories:
            current_weights[cat] = get_asset_value(cat) / total_value if total_value > 0 else 0

        # Target allocation from snapshot (equity, debt, cash)
        target_allocation = {
            "equity": asset_allocation.get("equity", 0) / 100,
            "debt": asset_allocation.get("debt", 0) / 100,
            "cash": asset_allocation.get("cash", 0) / 100,
        }

        # Map categories to equity, debt, cash for comparison
        category_map = {
            "mutual_funds": "equity",
            "stocks": "equity",
            "epf": "debt",
            "fixed_deposits": "debt",
            "bank_balance": "cash",
            "real_estate": "cash"
        }

        # Aggregate current weights by category type
        aggregated_weights = {"equity": 0, "debt": 0, "cash": 0}
        for cat, cat_type in category_map.items():
            aggregated_weights[cat_type] += current_weights.get(cat, 0)

        # Determine rebalance actions per category
        rebalance_actions = []
        for cat_type in ["equity", "debt", "cash"]:
            current_wt = aggregated_weights.get(cat_type, 0)
            target_wt = target_allocation.get(cat_type, 0)
            diff = target_wt - current_wt
            action = "Hold"
            if diff > 0.05:
                action = "Buy"
            elif diff < -0.05:
                action = "Sell"
            rebalance_actions.append(
                PortfolioRebalanceAction(
                    asset=cat_type,
                    current_weight=round(current_wt * 100, 2),
                    target_weight=round(target_wt * 100, 2),
                    action=action,
                    amount=round(abs(diff) * total_value, 2) if action != "Hold" else None
                )
            )

        # Asset allocation analysis based on age and risk profile
        # Simple heuristic for recommended allocation
        recommended_allocation = {}
        if risk_profile == "conservative":
            recommended_allocation = {"equity": 0.3, "debt": 0.5, "cash": 0.2}
        elif risk_profile == "aggressive":
            recommended_allocation = {"equity": 0.7, "debt": 0.2, "cash": 0.1}
        else:  # moderate
            recommended_allocation = {"equity": 0.5, "debt": 0.3, "cash": 0.2}

        allocation_analysis = AssetAllocationAnalysis(
            age=age,
            risk_profile=risk_profile,
            recommended_allocation={k: v * 100 for k, v in recommended_allocation.items()}
        )

        # SIP market timing adjustment suggestion (static market conditions)
        sip_adjustment = SIPAdjustmentSuggestion(
            suggestion="Maintain your current SIP amounts as market conditions are stable."
        )

        return InvestmentStrategyOutput(
            rebalance_actions=rebalance_actions,
            allocation_analysis=allocation_analysis,
            sip_adjustment=sip_adjustment
        )

    def default_input(self, context: ToolContext) -> InvestmentStrategyInput:
        data = load_mcp_snapshot()
        if data is None:
            raise FileNotFoundError("mcp_snapshot.json not found.")
        return InvestmentStrategyInput(financial_data=data)
