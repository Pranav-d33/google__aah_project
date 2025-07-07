import streamlit as st
import pandas as pd

def display_net_worth_trend(snapshot):
    net_worth_history = snapshot.get("net_worth_history", [])
    if not net_worth_history:
        st.warning("No net worth history data available.")
        return

    df = pd.DataFrame(net_worth_history)
    df['month'] = pd.to_datetime(df['month'])
    df = df.sort_values('month')

    st.line_chart(data=df.set_index('month')['value'], use_container_width=True)
