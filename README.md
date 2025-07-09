# 🏆 Lakshya - AI-Powered Personal Finance Agent

*Your premium financial assistant for sophisticated wealth management*

## 🌟 Overview

**Lakshya** is an advanced AI-powered personal finance agent that provides comprehensive financial analysis, investment guidance, and wealth management insights. Built with cutting-edge LangChain and Google Gemini AI technology, Lakshya offers personalized financial advice through an elegant Streamlit interface.

## 🚀 Key Features

### 🤖 Intelligent Financial Agent
- **Multi-Tool Integration**: Leverages 6 specialized financial tools for comprehensive analysis
- **Data Processing**: Uses predefined financial data snapshots (Fi MCP integration currently under development)
- **Memory-Enabled Conversations**: Maintains context across interactions using Vertex RAG
- **Natural Language Processing**: Powered by Google Gemini 2.0 Flash for sophisticated understanding

### 💼 Financial Analysis Tools
1. **Loan Eligibility Checker** - Assess loan affordability based on income and liabilities
2. **SIP Performance Analyzer** - Evaluate mutual fund and SIP investment performance
3. **Net Worth Trend Analysis** - Track wealth growth over time with projections
4. **Anomaly Detection** - Identify unusual financial patterns and risks
5. **Data Fetcher** - Access predefined financial snapshots (Fi MCP integration in progress)
6. **Advanced Financial Planning** - Retirement projections and tax optimization

## 🏗️ Architecture

### Core Components

```
lakshya_agent/
├── 🚀 landing_page.py          # Main Streamlit application
├── 🤖 tools/                   # Financial analysis tools
│   ├── root_agent.py          # Central agent orchestrator
│   ├── loan_eligibility.py    # Loan assessment tool
│   ├── sip_performance.py     # SIP analysis tool
│   ├── net_worth_trend.py     # Wealth tracking tool
│   ├── anomaly_detection.py   # Risk detection tool
│   ├── fi_mcp_realtime.py     # Real-time data connector
│   └── fetch_financial_data.py # Data retrieval tool
├── 📊 components/              # UI components
│   ├── health_score.py        # Financial health calculator
│   ├── net_worth_trend.py     # Wealth visualization
│   ├── loan_calculator.py     # EMI calculator
│   └── emi_card.py           # EMI display component
├── 🔧 agent.yaml              # Agent configuration
├── 📄 requirements.txt        # Dependencies
└── 📋 mcp_snapshot.json       # Sample financial data
```

### Technology Stack
- **AI Framework**: LangChain + Google Gemini 2.0 Flash
- **Frontend**: Streamlit with custom CSS styling
- **Data Processing**: Pandas, NumPy
- **Memory**: Vertex RAG for conversation context
- **Visualization**: Plotly, Matplotlib
- **Data Source**: Predefined JSON snapshots (Fi MCP integration under development)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Google API Key for Gemini
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd google_aah_project
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r lakshya_agent/requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the `lakshya_agent` directory based on the provided `.env.example`:

```bash
# Copy the example file
cp lakshya_agent/.env.example lakshya_agent/.env
```

Then edit the `.env` file with your actual values:
```env
GOOGLE_API_KEY=your_google_api_key_here
MCP_URL=https://mcp.fi.money:8080/mcp/stream
PYTHONPATH="."
```

### 5. Data Setup
The application currently uses predefined financial data from `mcp_snapshot.json`. The Fi MCP real-time integration is under development.

**Note**: The MCP (Model Context Protocol) functionality for live financial data is currently not operational. All financial analysis tools use the predefined sample data provided in `mcp_snapshot.json` for demonstration purposes.

## 🚀 Running the Application

### Start the Streamlit App
```bash
cd lakshya_agent
streamlit run landing_page.py
```

The application will be available at `http://localhost:8501`

### Using the Application

1. **Landing Page**: 
   - View personalized financial insights
   - Access the AI chatbot for financial queries
   - Monitor key metrics like health score and EMI capacity

2. **Executive Dashboard**:
   - Detailed net worth analysis
   - Loan optimization calculator
   - Comprehensive financial health assessment

3. **Chat Interface**:
   - Ask natural language questions about finances
   - Get personalized investment advice
   - Receive loan eligibility assessments

## 📊 Sample Data Structure

**Important Note**: The application currently operates using predefined sample data. The Fi MCP (Model Context Protocol) integration for real-time financial data is under development and not currently functional.

The application uses a JSON snapshot format for financial data:

```json
{
  "user_profile": {
    "age": 21,
    "risk_profile": "moderate",
    "retirement_age": 60
  },
  "assets": {
    "bank_balance": 650000,
    "mutual_funds": [...],
    "stocks": [...],
    "epf": 125000,
    "fixed_deposits": [...],
    "real_estate": 2500000
  },
  "liabilities": {
    "home_loan": 1750000,
    "car_loan": 200000,
    "personal_loan": 50000
  },
  "income": {
    "monthly_salary": 80000,
    "rental_income": 20000
  },
  "expense_history": [...],
  "net_worth_history": [...]
}
```

## 🧠 AI Agent Capabilities

### Financial Analysis
- **Loan Affordability**: Calculate maximum loan amounts based on income and existing liabilities
- **SIP Optimization**: Analyze mutual fund performance and recommend adjustments
- **Risk Assessment**: Detect financial anomalies and provide alerts
- **Wealth Tracking**: Monitor net worth trends and project future growth

### Conversation Features
- **Context Awareness**: Remembers previous interactions and financial analyses
- **Tool Integration**: Seamlessly uses multiple financial tools to provide comprehensive answers
- **Personalization**: Adapts responses based on user's financial profile and history

### Example Queries
- "Am I eligible for a ₹50 lakh home loan?"
- "How are my SIPs performing this quarter?"
- "What's my current financial health score?"
- "Suggest ways to optimize my tax savings"
- "Show me my net worth trend over the last 6 months"

## 🔧 Configuration

### Agent Configuration (agent.yaml)
```yaml
name: lakshya-agent
description: Personal finance agent
model: gemini-2.0-flash
tools:
  - fetch_financial_data
  - sip_performance
  - loan_eligibility
  - net_worth_trend
  - anomaly_detection
  - fi_mcp_realtime
```

### Memory Configuration
- **Type**: Vertex RAG
- **Similarity Top-K**: 5
- **Vector Distance Threshold**: 0.7

## 🎯 Key Metrics & Calculations

### Financial Health Score
Weighted calculation based on:
- **Savings Rate** (30%): Monthly savings as % of income
- **Debt-to-Income Ratio** (30%): Total debt vs annual income
- **Investment Diversification** (20%): Asset allocation across categories
- **Liquidity Ratio** (20%): Liquid assets vs total debt

### EMI Affordability
- **Maximum EMI**: 35% of monthly salary (conservative approach)
- **Existing EMI Consideration**: Includes current loan obligations
- **Stress Testing**: Evaluates affordability under various scenarios

## 🔒 Security & Privacy

- Environment variables for API keys
- No sensitive data stored in repository
- Local data processing with optional cloud integration
- Secure API connections with proper authentication

## 🚦 Error Handling

The application includes comprehensive error handling:
- **Missing Data**: Graceful degradation with default values
- **MCP Connection**: Fallback to predefined sample data when Fi MCP is unavailable
- **Tool Errors**: Detailed error messages with recovery suggestions
- **Input Validation**: Robust validation for all user inputs

## ⚠️ Current Limitations

### Fi MCP Integration Status
- **Real-time Data**: Fi MCP integration is under development and currently not functional
- **Sample Data**: All financial analysis tools use predefined data from `mcp_snapshot.json`
- **Demo Mode**: The application operates in demonstration mode with sample financial profiles
- **Future Release**: Live financial data integration will be available in future updates

## 🧪 Testing

### Running Tests
```bash
pytest lakshya_agent/tests/
```

### Test Coverage
- Unit tests for all financial calculation tools
- Integration tests for agent workflows
- UI component testing for Streamlit interface

## 📈 Performance Optimization

- **Caching**: Streamlit caching for expensive operations
- **Lazy Loading**: Components loaded on demand
- **Memory Management**: Efficient data processing with pandas
- **API Rate Limiting**: Respectful API usage with proper throttling

## 🔄 Future Enhancements

### Planned Features
- [ ] **Fi MCP Integration**: Complete real-time financial data connectivity
- [ ] Real-time market data integration
- [ ] Advanced portfolio optimization algorithms
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Integration with banking APIs
- [ ] Advanced tax planning tools
- [ ] Social trading features

### Technical Improvements
- [ ] Microservices architecture migration
- [ ] Enhanced caching strategies
- [ ] Advanced ML models for predictions
- [ ] Blockchain integration for secure transactions

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Follow the existing code style
4. Write tests for new features
5. Submit a pull request

### Code Standards
- **Python**: PEP 8 compliance
- **Documentation**: Comprehensive docstrings
- **Testing**: Minimum 80% test coverage
- **Security**: Regular security audits


## 📞 Support

For support, issues, or feature requests:
- Create an issue on GitHub
- Contact the development team
- Check the documentation for troubleshooting

---

*Built with ❤️ for the future of personal finance management*


## 📊 Demo

https://lakshya-ai.streamlit.app/
---

**Happy Financial Planning with Lakshya! 🚀**
