import streamlit as st

def calculate_financial_health_score(snapshot):
    income = snapshot.get("income", {})
    liabilities = snapshot.get("liabilities", {})
    assets = snapshot.get("assets", {})
    contributions = snapshot.get("contributions", {})
    emergency_fund = snapshot.get("emergency_fund", 0)

    monthly_salary = income.get("monthly_salary", 0)
    total_debt = sum(liabilities.values())
    total_assets = 0
    for key, val in assets.items():
        if isinstance(val, list):
            total_assets += sum(item.get("current_value", 0) if isinstance(item, dict) else 0 for item in val)
        elif isinstance(val, (int, float)):
            total_assets += val

    savings_percent = (contributions.get("monthly_savings", 0) / monthly_salary * 100) if monthly_salary > 0 else 0
    debt_to_income = (total_debt / (monthly_salary * 12) * 100) if monthly_salary > 0 else 0
    liquidity_ratio = (assets.get("bank_balance", 0) + emergency_fund) / total_debt if total_debt > 0 else 1

    # Investment diversification: count number of asset categories with >5% allocation
    categories = ["mutual_funds", "stocks", "epf", "fixed_deposits", "real_estate"]
    diversified_count = 0
    for cat in categories:
        val = assets.get(cat, 0)
        total_val = 0
        if isinstance(val, list):
            total_val = sum(item.get("current_value", 0) if isinstance(item, dict) else 0 for item in val)
        elif isinstance(val, (int, float)):
            total_val = val
        if total_assets > 0 and (total_val / total_assets) > 0.05:
            diversified_count += 1
    diversification_score = (diversified_count / len(categories)) * 100

    # Calculate weighted score out of 100
    score = (
        0.3 * min(savings_percent, 100) +
        0.3 * max(0, 100 - debt_to_income) +
        0.2 * diversification_score +
        0.2 * min(liquidity_ratio * 100, 100)
    )
    return round(score, 2)

def get_health_score_zone(score):
    if score >= 75:
        return "green", "Healthy"
    elif score >= 50:
        return "yellow", "Caution"
    else:
        return "red", "Critical"

def display_health_score(snapshot):
    score = calculate_financial_health_score(snapshot)
    zone, zone_label = get_health_score_zone(score)
    zone_color = {"green": "#28a745", "yellow": "#ffc107", "red": "#dc3545"}[zone]
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;">
            <span style="font-size:2.5rem;font-weight:700;color:{zone_color};margin-right:0.5rem;">{score}</span>
            <span style="font-size:1.2rem;font-weight:600;color:{zone_color};">{zone_label} Zone</span>
        </div>
        <div style="color:#aaa;font-size:0.95rem;margin-bottom:1.2rem;">Financial Health Score (out of 100)</div>
        """,
        unsafe_allow_html=True
    )