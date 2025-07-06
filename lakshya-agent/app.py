import streamlit as st
from tools.root_agent import invoke_agent

# --- Page Configuration ---
st.set_page_config(
    page_title="Lakshya Financial Agent",
    page_icon="💰",
    layout="wide"
)

# --- Title and Description ---
st.title("Lakshya - Your Personal Financial Agent 🤖")
st.markdown("Welcome! I can help you with your financial questions. Try asking about loan eligibility, SIP performance, your net worth, and more.")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you with your finances today?"}
    ]

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("Ask your financial question here..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Generate and Display Agent Response ---
    with st.chat_message("assistant"):
        with st.spinner("Lakshya is thinking..."):
            try:
                # This assumes your agent has a function `invoke_agent`
                # that takes the user's query and returns a response.
                # You might need to adjust this part to fit your agent's code.
                response = invoke_agent(prompt)
                st.markdown(response)
                # Add agent response to session state
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"Sorry, an error occurred: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# --- Sidebar (Optional) ---
with st.sidebar:
    st.header("About")
    st.write("This is a Streamlit interface for the Lakshya financial agent.")
    st.write("The agent uses a suite of tools to answer your financial queries.")
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you with your finances today?"}
        ]
        st.rerun()