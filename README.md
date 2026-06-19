# FINWISE: Your Autonomous AI Financial Advisor

FINWISE is a comprehensive, AI-driven personal financial management and advisory platform. By combining traditional financial metrics with advanced machine learning (Random Forest) and generative AI (Llama-3 via LangChain), FINWISE acts as your personal CFO, Coach, and Financial Planner.

## 🌟 Overview
FINWISE moves beyond simple expense tracking. It predicts financial risks, assesses your holistic financial health, identifies your behavioral persona, and generates real-time, actionable coaching plans. Whether you are a "Student Saver" or a "Wealth Builder", FINWISE adapts its roadmap to your life stage.

## 🚀 Features
- **Authentication**: Secure user login and registration.
- **Financial Assessment**: Deep dive into your monthly cashflow.
- **Random Forest Risk Prediction**: ML-based early warning system for bankruptcy or debt traps.
- **Dashboard Analytics**: Comprehensive visualization of your financial trajectory.
- **Financial Health Score**: Composite score evaluating debt, savings, and expenses.
- **Financial Goals & Emergency Fund Planner**: Track your dreams with smart prioritization.
- **AI Personalized Coach & AI Advisor**: Conversational LangChain agent acting as a Certified Financial Planner.
- **Financial Benchmarking & Maturity Level**: Compare your stats against ideal standards.
- **Cashflow Intelligence Suite**: Forecast future balances based on historical trends.
- **Smart Budgeting & Habit Tracking**: Enforce discipline with streak tracking.
- **Gamification (XP, Levels, Challenges)**: Earn badges and XP by completing weekly financial challenges.
- **AI Life Planning & Financial Roadmap**: Generate 1, 3, and 5-year life plans.
- **Investment Readiness Analysis**: Gatekeeper to ensure you are safe before investing.
- **Financial Education Hub**: Tailor-made learning curriculum based on your financial weaknesses.
- **Advanced Financial Simulation**: "What-If" scenario planning (e.g., +20% income, debt payoffs).
- **PDF Reporting**: End-of-month holistic PDF export.

## 🛠 Technology Stack
- **Frontend**: Streamlit (Python)
- **Backend**: Python 3.10+
- **Database**: MySQL (Relational Data Persistence)
- **Machine Learning**: Scikit-Learn (Random Forest Classifier)
- **AI / LLM**: LangChain, ChatGroq (Llama-3 70B/8B)
- **PDF Generation**: ReportLab
- **Data Analysis**: Pandas, NumPy

## 🏗 Architecture
FINWISE is built on a modular architecture:
1.  **Presentation Layer**: Streamlit pages (`pages/*.py`).
2.  **Logic & Engine Layer**: Modularized engines (`xp_engine.py`, `roadmap_engine.py`, `investment_engine.py`, `learning_engine.py`, `persona_engine.py`, `challenge_engine.py`).
3.  **Intelligence Layer**: `model_trainer.py` (Random Forest) and `langchain_service.py` (LLM Integration).
4.  **Data Access Layer**: `db.py` (MySQL CRUD operations).

## 💻 Installation
1.  Clone the repository.
2.  Create a virtual environment: `python -m venv venv`
3.  Activate the environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows).
4.  Install dependencies: `pip install -r requirements.txt`
5.  Set up environment variables: `cp .env.example .env` and fill in your `GROQ_API_KEY` and MySQL credentials.

## 🗄 Database Setup
1.  Ensure MySQL is running.
2.  Create database: `CREATE DATABASE finwise;`
3.  Run all SQL migrations located in the root directory.

## 🧠 AI & Machine Learning Components
- **Machine Learning**: A pre-trained Random Forest model (`financial_risk_model.pkl`) evaluates 3 core features (Debt Ratio, Expense Ratio, Saving Rate) to classify users into "Aman", "Waspada", or "Berbahaya".
- **Generative AI**: Groq's Llama-3 model acts as the brain for the AI Coach, utilizing dynamic context prompts assembled by the various engines.

## 🔮 Future Development
- Integration with live bank APIs (Open Banking).
- Joint/Family accounts for household financial planning.
- Complex compound interest simulators for stock/crypto portfolios.

---
*Built with ❤️ by the FINWISE Team.*
