from google.adk.agents import Agent
from google.adk.models import Gemini
from .fetch_financial_data import FetchFinancialDataTool
from .sip_performance import SIPPerformanceTool
from .loan_eligibility import LoanEligibilityTool
from .net_worth_trend import NetWorthTrendTool
from .anomaly_detection import AnomalyDetectionTool
from .fi_mcp_realtime import FiMCPRealtimeTool
from google.adk.runners import Runner
#from google.adk.memory import InMemoryMemoryService
from google.adk.memory import VertexAiRagMemoryService

memory = VertexAiRagMemoryService(
    rag_corpus="projects/YOUR_PROJECT_ID/locations/REGION/ragCorpora/lakshya",
    similarity_top_k=5,
    vector_distance_threshold=0.7
)

root_agent = Agent(
    name="lakshya_agent",
    description="A personal finance agent that analyzes data and offers intelligent financial guidance.",
    instruction=(
        """You are Lakshya, a helpful and reliable AI finance co-pilot that gives personalized answers using the user's real financial data.

  You have access to tools that fetch user data, analyze SIPs, detect anomalies, assess loan eligibility, and check net worth trends. Whenever possible, prefer using these tools rather than guessing or answering generically.

  If a user asks something like:
  - “Can I afford a ₹50L loan?”
  - “How are my SIPs doing?”
  - “What changed in my net worth?”
  - “Any red flags in my finances?”

  → You MUST use tools to generate accurate, data-driven insights.

  You can also retrieve past tool outputs using memory to improve continuity. Mention prior decisions or summaries if relevant.

  Avoid giving disclaimers like “I’m just an AI.” Focus on being useful, confident, and grounded in real user data."""
    ),
    model=Gemini(model_name="gemini-2.0-flash"),
    tools=[
        FetchFinancialDataTool(),
        SIPPerformanceTool(),
        LoanEligibilityTool(),
        NetWorthTrendTool(),
        AnomalyDetectionTool(),
        FiMCPRealtimeTool()
        # Add more tools here as you implement them
    ],
     
)
