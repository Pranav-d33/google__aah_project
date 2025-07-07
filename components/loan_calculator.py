import streamlit as st

def calculate_emi(principal, annual_rate, years):
    monthly_rate = annual_rate / (12 * 100)
    months = years * 12
    emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / (((1 + monthly_rate) ** months) - 1)
    return emi

def display_loan_calculator(snapshot):
    income = snapshot.get("income", {})
    monthly_salary = income.get("monthly_salary", 0)

    st.write("Enter loan details to calculate affordability and EMI feasibility:")

    loan_amount = st.number_input("Loan Amount (₹)", min_value=0, value=1000000, step=100000)
    tenure_years = st.number_input("Loan Tenure (Years)", min_value=1, max_value=30, value=20)
    interest_rate = st.number_input("Interest Rate (%)", min_value=0.1, max_value=20.0, value=8.0, step=0.1)

    if monthly_salary == 0:
        st.warning("Monthly salary data not found in snapshot. Loan affordability cannot be calculated.")
        return

    max_affordable_emi = monthly_salary * 0.35
    emi = calculate_emi(loan_amount, interest_rate, tenure_years)

    st.write(f"Maximum Affordable EMI (35% of salary): ₹{max_affordable_emi:,.2f}")
    st.write(f"Calculated EMI for loan: ₹{emi:,.2f}")

    if emi <= max_affordable_emi:
        st.success("You can afford this loan based on your current income.")
    else:
        st.error("This loan may not be affordable based on your current income.")
