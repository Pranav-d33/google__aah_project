import streamlit as st

def display_additional_insights(snapshot):
    user_profile = snapshot.get("user_profile", {})
    age = user_profile.get("age", 0)
    retirement_age = user_profile.get("retirement_age", 60)

    emergency_fund = snapshot.get("emergency_fund", 0)
    expense_history = snapshot.get("expense_history", [])
    avg_monthly_expenses = 0
    if expense_history:
        total_expenses = sum(item.get("expenses", 0) for item in expense_history)
        avg_monthly_expenses = total_expenses / len(expense_history)

    asset_allocation = snapshot.get("asset_allocation", {})
    equity_allocation = asset_allocation.get("equity", 0)

    # Insight 1: Retirement projection
    years_to_retirement = retirement_age - age
    if years_to_retirement > 0:
        retirement_msg = f"You’re on track to retire by {retirement_age} (in {years_to_retirement} years)."
    else:
        retirement_msg = f"You have reached or passed your retirement age of {retirement_age}."

    # Insight 2: Cash reserve duration
    if avg_monthly_expenses > 0:
        months_cash_reserve = emergency_fund / avg_monthly_expenses
        cash_reserve_msg = f"Your cash reserve can last {months_cash_reserve:.1f} months without income."
    else:
        cash_reserve_msg = "Insufficient expense data to calculate cash reserve duration."

    # Insight 3: Equity allocation warning (example recommendation: 50% equity for age < 30, 40% for 30-50, 30% for >50)
    recommended_equity = 50 if age < 30 else 40 if age <= 50 else 30
    if equity_allocation < recommended_equity:
        equity_msg = f"Equity allocation ({equity_allocation}%) is below recommended ({recommended_equity}%) for your age."
    else:
        equity_msg = f"Equity allocation ({equity_allocation}%) is within the recommended range for your age."

    st.subheader("Additional Personalized Insights")
    st.write(f"- {retirement_msg}")
    st.write(f"- {cash_reserve_msg}")
    st.write(f"- {equity_msg}")
