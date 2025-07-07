import streamlit as st
import sys
import os
import json

# --- Path Setup & Imports ---
# Add project root to path to allow imports from other directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import agent and component functions
from tools.root_agent import invoke_agent
from tools.mcp_loader import load_mcp_snapshot
from components.health_score import display_health_score, calculate_financial_health_score, get_health_score_zone
from components.net_worth_trend import display_net_worth_trend
from components.loan_calculator import display_loan_calculator

# --- Page Configuration & Styling ---
st.set_page_config(
    page_title="Lakshya - Financial Agent",
    layout="wide"
)

# --- Elegant Luxury Theme using CSS ---
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap');
    
    /* Core App Styling - Luxury Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #2a2a2a 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }

    /* Main Headers - Luxury Gold Accent */
    h1 {
        color: #d4af37 !important; /* Luxury Gold */
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        font-size: 3.5rem !important;
        text-align: center !important;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 4px rgba(212, 175, 55, 0.3);
    }

    h2 {
        color: #f5f5f5 !important; /* Elegant White */
        font-family: 'Playfair Display', serif !important;
        font-weight: 600 !important;
        font-size: 2.2rem !important;
        margin-bottom: 1.5rem !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    }

    h3 {
        color: #e8e8e8 !important; /* Soft White */
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 1.4rem !important;
        margin-bottom: 1rem !important;
    }

    /* Subheaders */
    .stMarkdown h4 {
        color: #d4af37 !important; /* Luxury Gold */
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    /* Regular text - Premium Typography */
    .stMarkdown p {
        color: #cccccc !important; /* Elegant Gray */
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        font-weight: 400 !important;
    }

    /* Welcome Message Styling */
    .stMarkdown p strong {
        color: #d4af37 !important; /* Gold for emphasis */
        font-weight: 600 !important;
    }

    /* Buttons - Luxury Style */
    .stButton>button {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        color: #000000 !important;
        border-radius: 12px !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        padding: 0.75rem 2rem !important;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #b8941f 0%, #d4af37 100%) !important;
        color: #000000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4) !important;
    }

    /* Chat Input - Elegant Dark */
    .stChatInput {
        background: rgba(42, 42, 42, 0.95) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        margin-top: 1rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Chat Input Text */
    .stChatInput input {
        background-color: transparent !important;
        color: #ffffff !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem !important;
    }

    /* Chat Input Placeholder */
    .stChatInput input::placeholder {
        color: #888888 !important;
        font-style: italic !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Chat Input Submit Button */
    .stChatInput button {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        color: #000000 !important;
        padding: 0.5rem !important;
        margin-left: 0.5rem !important;
        box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stChatInput button:hover {
        background: linear-gradient(135deg, #b8941f 0%, #d4af37 100%) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 3px 12px rgba(212, 175, 55, 0.4) !important;
    }

    /* Chat Messages Container */
    [data-testid="stChatMessageContainer"] {
        background: rgba(42, 42, 42, 0.9) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }

    /* Chat Messages - Luxury Cards */
    .stChatMessage {
        background: rgba(42, 42, 42, 0.9) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }

    /* User Messages - Distinct Styling */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.15) 0%, rgba(184, 148, 31, 0.15) 100%) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        margin-left: 2rem !important;
        margin-right: 0 !important;
    }

    /* Assistant Messages - Distinct Styling */
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(42, 42, 42, 0.9) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        margin-left: 0 !important;
        margin-right: 2rem !important;
    }

    /* Chat Message Text */
    .stChatMessage p {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        margin: 0 !important;
    }

    /* Chat Message Content */
    .stChatMessage .stMarkdown {
        color: #ffffff !important;
    }

    /* Chat Message Content Paragraphs */
    .stChatMessage .stMarkdown p {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        margin-bottom: 0.5rem !important;
    }

    /* Chat Message Strong Text */
    .stChatMessage .stMarkdown strong {
        color: #d4af37 !important;
        font-weight: 600 !important;
    }

    /* Chat Message Lists */
    .stChatMessage .stMarkdown ul {
        margin-left: 1rem !important;
        margin-bottom: 1rem !important;
    }

    .stChatMessage .stMarkdown li {
        color: #cccccc !important;
        margin-bottom: 0.3rem !important;
    }

    /* Chat Avatar Styling */
    .stChatMessage > div:first-child {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%) !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-right: 1rem !important;
        box-shadow: 0 2px 8px rgba(212, 175, 55, 0.3) !important;
    }

    /* Chat Flow Container */
    .stChatFloatingInputContainer {
        background: rgba(26, 26, 26, 0.95) !important;
        border-top: 1px solid rgba(212, 175, 55, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        padding: 1rem !important;
    }

    /* Metric Styling - Luxury Cards */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(42, 42, 42, 0.95) 0%, rgba(60, 60, 60, 0.95) 100%) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.2) !important;
        border-color: rgba(212, 175, 55, 0.5) !important;
    }

    /* Metric Labels */
    [data-testid="metric-container"] > div:first-child {
        color: #d4af37 !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 0.5rem !important;
    }

    /* Metric Values */
    [data-testid="metric-container"] > div:last-child {
        color: #ffffff !important;
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    }

    /* Info boxes - Luxury Style */
    .stInfo {
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.1) 0%, rgba(184, 148, 31, 0.1) 100%) !important;
        border: 1px solid rgba(212, 175, 55, 0.4) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 1.5rem !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }

    /* Sidebar and Container Styling */
    .stContainer {
        background: rgba(26, 26, 26, 0.8) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        margin-bottom: 2rem !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
        backdrop-filter: blur(10px) !important;
    }

    /* Divider Styling */
    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.5), transparent) !important;
        margin: 2rem 0 !important;
    }

    /* Spinner Styling */
    .stSpinner {
        color: #d4af37 !important;
    }

    /* Success/Error Messages */
    .stSuccess {
        background: rgba(40, 167, 69, 0.1) !important;
        border: 1px solid rgba(40, 167, 69, 0.3) !important;
        color: #28a745 !important;
        border-radius: 12px !important;
    }

    .stError {
        background: rgba(220, 53, 69, 0.1) !important;
        border: 1px solid rgba(220, 53, 69, 0.3) !important;
        color: #dc3545 !important;
        border-radius: 12px !important;
    }

    .stWarning {
        background: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        color: #ffc107 !important;
        border-radius: 12px !important;
    }

    /* Custom List Styling */
    .stMarkdown ul {
        padding-left: 0 !important;
        list-style: none !important;
    }

    .stMarkdown li {
        color: #cccccc !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.8 !important;
        margin-bottom: 0.5rem !important;
        padding-left: 1.5rem !important;
        position: relative !important;
    }

    .stMarkdown li:before {
        content: "◆" !important;
        color: #d4af37 !important;
        font-size: 0.8rem !important;
        position: absolute !important;
        left: 0 !important;
        top: 0.1rem !important;
    }

    /* Column Spacing */
    .stColumn {
        padding: 0 1rem !important;
    }
</style>
""", unsafe_allow_html=True)



def get_asset_value(asset):
    if isinstance(asset, list):
        return sum(item.get("current_value", 0) if isinstance(item, dict) else 0 for item in asset)
    elif isinstance(asset, (int, float)):
        return asset
    return 0


def get_financial_insights(snapshot):
    """
    Computes personalized insights from the mcp_snapshot.json data.
    Uses the same health score logic as the dashboard for consistency.
    """
    insights = {}

    # Use the shared health score function
    score = calculate_financial_health_score(snapshot)
    zone, zone_label = get_health_score_zone(score)
    insights['health_score'] = f"{score}/100"
    insights['health_zone'] = zone
    insights['health_zone_label'] = zone_label

    # Calculate EMI and cash reserve as before
    income = snapshot.get('income', {}).get('monthly_salary', 0) or snapshot.get('monthly_income', 0) or 75000
    expenses = snapshot.get('expenses', {}).get('total_monthly_expenses', 0) or snapshot.get('monthly_expenses', 0) or 45000
    assets = snapshot.get('assets', {}) or {
        'cash': 50000,
        'savings_account': 200000,
        'stocks': 300000,
        'mutual_funds': 150000,
        'real_estate': 2000000
    }
    surplus = income - expenses
    max_emi = surplus * 0.40 if surplus > 0 else 0
    insights['max_emi'] = f"₹{max_emi:,.0f}"

    liquid_assets = assets.get('cash', 0) + assets.get('savings_account', 0)
    reserve_months = liquid_assets / expenses if expenses > 0 else 0
    insights['cash_reserve'] = f"{reserve_months:.1f} months"

    stocks_val = get_asset_value(assets.get('stocks', 0))
    mf_val = get_asset_value(assets.get('mutual_funds', 0))
    investments = stocks_val + mf_val
    if investments > 500000:
        insights['retirement_insight'] = "Your investment portfolio shows excellent diversification for long-term wealth building."
    elif investments > 100000:
        insights['retirement_insight'] = "Consider increasing equity allocation for enhanced retirement planning."
    else:
        insights['retirement_insight'] = "Building a robust investment portfolio is recommended for future financial goals."
    return insights

# --- UI Rendering Functions ---

def display_landing_page(snapshot):
    """Renders the main landing page with chatbot and insights."""
    st.title("Lakshya")
    st.markdown("**Welcome to your premium financial experience.** Ask sophisticated questions or explore your personalized wealth insights below.")

    # --- Reversed Layout: Insights on Left, Chat on Right ---
    col1, col2 = st.columns([1.3, 2]) # Insights column slightly wider, chat on right

    with col1:
        # --- Personalized Insights Section ---
        st.header("Wealth Insights")
        insights = get_financial_insights(snapshot)
        score = float(insights['health_score'].split('/')[0])
        zone = insights['health_zone']
        zone_label = insights['health_zone_label']
        zone_color = {"green": "#28a745", "yellow": "#ffc107", "red": "#dc3545"}[zone]

        # Unified health score display
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

        st.metric(
            label="🏆 Maximum Affordable EMI",
            value=insights['max_emi'],
            help="40% of your surplus monthly income for optimal financial health"
        )
        st.metric(
            label="🛡️ Emergency Reserve",
            value=insights['cash_reserve'],
            help="Liquid assets coverage based on monthly expenses"
        )

        st.markdown("---")
        st.subheader("Wealth Advisory")
        st.info(insights['retirement_insight'])

        st.markdown("---")

        if st.button("View Executive Dashboard", type="primary"):
            st.session_state.view = 'dashboard'
            st.rerun()

        st.subheader("How may I assist you today?")
        st.markdown("""
        **• Strategic savings optimization**  
        **• Portfolio rebalancing strategies**  
        **• Tax efficiency planning**  
        **• Investment timing optimization**
        """)

    with col2:
        # --- Agent Chatbot Interface ---
        st.header("Financial Advisor")

        # Create a styled container for the chat area
        with st.container():
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "assistant", "content": "Good day! I'm here to provide sophisticated financial guidance tailored to your wealth management needs. How may I assist you?"}]

            # Display chat history in a scrollable container
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # User input at the bottom
            if prompt := st.chat_input("Ask about investments, wealth planning, portfolio optimization..."):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # Generate and display agent response
                with st.chat_message("assistant"):
                    with st.spinner("Analyzing your financial query..."):
                        try:
                            response = invoke_agent(prompt)
                            st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        except Exception as e:
                            error_message = (
                                "Sorry, an error occurred while processing your request. "
                                "Please try again or rephrase your question."
                            )
                            st.error(error_message)
                            st.session_state.messages.append({"role": "assistant", "content": error_message})

def display_full_dashboard(snapshot):
    """Renders the detailed dashboard view."""
    st.title("Executive Financial Dashboard")

    if st.button("← Return to Home", type="primary"):
        st.session_state.view = 'landing'
        st.rerun()

    st.header("Net Worth Analysis")
    display_net_worth_trend(snapshot)

    st.header("Loan Optimization Calculator")
    display_loan_calculator(snapshot)

    st.header("Comprehensive Financial Health Assessment")
    display_health_score(snapshot)


# --- Main Application Logic ---
def main():
    # Initialize view state
    if 'view' not in st.session_state:
        st.session_state.view = 'landing'

    # Load data once
    snapshot = load_mcp_snapshot()
    if snapshot is None:
        st.error("mcp_snapshot.json not found. Please ensure the file is present in the project root.")
        return

    # Render the appropriate view
    if st.session_state.view == 'landing':
        display_landing_page(snapshot)
    elif st.session_state.view == 'dashboard':
        display_full_dashboard(snapshot)

if __name__ == "__main__":
    main()