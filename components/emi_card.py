import streamlit as st

def calculate_emi(principal, annual_rate, years):
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12
    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
    return emi

def display_emi_card(snapshot, preferred_loan_term=20, preferred_interest_rate=8.0):
    income = snapshot.get("income", {})
    monthly_salary = income.get("monthly_salary", 0)
    expenses_history = snapshot.get("expense_history", [])
    avg_monthly_expenses = 0
    if expenses_history:
        total_expenses = sum(item.get("expenses", 0) for item in expenses_history)
        avg_monthly_expenses = total_expenses / len(expenses_history)

    max_affordable_emi = monthly_salary * 0.35 if monthly_salary else 0
    # For demonstration, assume principal = max affordable EMI * loan term * 12 (approximate max loan amount)
    principal = max_affordable_emi * preferred_loan_term * 12
    emi = calculate_emi(principal, preferred_interest_rate, preferred_loan_term)

    st.subheader("Maximum Affordable EMI")
    st.metric(label="Max Affordable EMI (35% of salary)", value=f"₹{max_affordable_emi:,.2f}")
    st.metric(label=f"Estimated EMI for ₹{principal:,.0f} loan at {preferred_interest_rate}% for {preferred_loan_term} years", value=f"₹{emi:,.2f}")

    if emi <= max_affordable_emi:
        st.success("You can afford this loan based on your current income.")
    else:
        st.error("This loan may not be affordable based on your current income.")
