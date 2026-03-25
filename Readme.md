# ⚡ AI-Powered Executive Email Assistant

An intelligent backend system and dashboard that automates email intent extraction using **Google Gemini 2.0 Flash**. This project transforms a cluttered Gmail inbox into a structured, actionable schedule.

![Dashboard Screenshot](s.PNG)

## 🚀 Key Features
- **Intelligent Intent Classification:** Uses LLM orchestration to distinguish between `SCHEDULING` (meetings/appointments) and `UPDATE` (status reports/info).
- **Automated Entity Extraction:** Automatically parses meeting times, participants, and summaries into structured JSON.
- **Robust Email Parsing:** Handles complex Multipart MIME (HTML/Plain Text) email structures.
- **Performance Optimized:** Implements client-side caching (`st.cache_data`) to manage API rate limits and reduce latency.
- **Security First:** Designed with strict environment variable management and OAuth 2.0 flow.

## 🛠️ Tech Stack
- **Language:** Python 3.12
- **AI Engine:** Google GenAI (Gemini 2.0 Flash)
- **Framework:** Streamlit (Frontend Dashboard)
- **APIs:** Google Gmail API, Google Auth
- **Environment:** Dotenv for Secret Management

## 📂 Project Structure
```text
ai-email-assistant/
├── src/
│   ├── agent.py           # Gemini AI Logic & Prompt Engineering
│   ├── gmail_service.py   # Gmail API Integration & MIME Parsing
├── dashboard.py           # Streamlit UI & Caching Layer
├── .env                   # API Keys (Local Only)
├── .gitignore             # Security Filter
└── requirements.txt       # Dependencies