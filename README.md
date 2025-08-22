📈 AI Stock Research Tool
Multi-Agent AI System for Intelligent Stock Analysis & Trading Recommendations

A sophisticated financial analysis platform that leverages CrewAI's multi-agent orchestration to deliver comprehensive stock research through specialized AI agents. Built with modern Python frameworks and real-time market data integration. app.py:14-15

🚀 Key Features
🤖 Multi-Agent AI Architecture: Specialized analyst and trader agents working collaboratively
📊 Real-Time Market Data: Live stock prices, volume, and historical trends via Yahoo Finance
🎯 Intelligent Recommendations: AI-powered Buy/Sell/Hold decisions with detailed rationale
📈 Interactive Visualizations: Dynamic charts with moving averages and volume analysis
🌐 Dual Interface: Both web UI and CLI for different use cases
📰 News Integration: Latest market news and headlines
⚡ Multi-Stock Comparison: Side-by-side analysis of multiple stocks app.py:16-24
🛠️ Tech Stack
Core Framework
CrewAI (0.140.0) - Multi-agent orchestration and task management
Python 3.11+ - Modern Python runtime with type hints
Streamlit - Interactive web application framework crew.py:1
AI & Data
Groq LLM (llama-3.3-70b-versatile) - Advanced language model for analysis
yfinance (0.2.64) - Real-time financial data API
pandas - Data manipulation and analysis app.py:8-9
Infrastructure
SQLite3 - Local data persistence
python-dotenv - Environment configuration management
Docker Dev Container - Consistent development environment app.py:1-3
🏗️ System Architecture















crew.py:8-12

🎯 Core Modules
1. Multi-Agent Orchestration (crew.py)
Central coordination hub that manages AI agent collaboration and task execution. crew.py:8-12

2. Web Application (app.py)
Feature-rich Streamlit interface with real-time data visualization and interactive analysis. app.py:29

3. AI Agent System
Analyst Agent: Processes market data and generates performance insights
Trader Agent: Evaluates trading opportunities and provides strategic recommendations analyse_task.py:5-19
4. Task Framework
Analysis Task: Comprehensive stock performance evaluation
Trading Task: Strategic decision-making with risk assessment trade_task.py:4-17
🚀 Quick Start
Prerequisites
Python 3.11+
Groq API Key (Get one here)
Installation
# Clone the repository  
git clone https://github.com/shubhamsinha1010/stock-analysis-crew-ai.git  
cd stock-analysis-crew-ai  
  
# Install dependencies  
pip install -r requirements.txt  
  
# Configure environment  
echo "GROQ_API_KEY=your_api_key_here" > .env
app.py:11-12

Run the Application
🌐 Web Interface (Recommended)

streamlit run app.py
Access at http://localhost:8501

💻 CLI Interface

python main.py
main.py:6-8

🎨 User Experience
Multi-Stock Comparison
Analyze multiple stocks side-by-side with real-time metrics, charts, and AI recommendations. app.py:22-24

Comprehensive Analysis
📊 Performance Metrics: Current price, daily change, volume analysis
📈 Technical Charts: 6-month price history with moving averages
🤖 AI Insights: Intelligent analysis from specialized agents
📰 Market News: Latest headlines and market sentiment app.py:60-64
🔧 Development Setup
Dev Container (VS Code)
Pre-configured development environment with all dependencies and auto-start capabilities. devcontainer.json:20-22

Manual Setup
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
pip install -r requirements.txt
🌟 Why This Project Stands Out
🚀 Cutting-Edge AI: Leverages latest CrewAI framework for multi-agent collaboration
📊 Real-World Application: Solves actual financial analysis challenges
🏗️ Scalable Architecture: Clean separation of concerns with modular design
🎯 Production Ready: Includes Docker containers, environment management, and error handling
📈 Data-Driven: Integrates real-time market data with AI-powered insights
