import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


from .loan_eligibility import check_loan_eligibility
from .sip_performance import get_sip_performance
from .net_worth_trend import get_net_worth_trend
from .fi_mcp_realtime import get_fi_mcp_realtime
from .anomaly_detection import detect_anomaly
from .fetch_financial_data import fetch_financial_data
from dotenv import load_dotenv
load_dotenv()


tools = [
    check_loan_eligibility,
    get_sip_performance,
    get_net_worth_trend,
    get_fi_mcp_realtime,
    detect_anomaly,
    fetch_financial_data,
]

# --- Agent Prompt Template ---
template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
prompt = PromptTemplate.from_template(template)


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.environ["GOOGLE_API_KEY"]
)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Main Agent Invocation Function ---
def invoke_agent(user_query: str):
    """
    Invokes the financial agent with a user query.
    """
    try:
        response = agent_executor.invoke({"input": user_query})
        return response.get("output", "I couldn't find an answer.")
    except Exception as e:
        return f"An error occurred while processing your request: {e}"

# You can add a simple test here to run this file directly
if __name__ == '__main__':
    test_query = "Am I eligible for a loan with an income of 50000 and a credit score of 750?"
    print(f"Testing agent with query: '{test_query}'")
    result = invoke_agent(test_query)
    print("Agent Response:")
    print(result)