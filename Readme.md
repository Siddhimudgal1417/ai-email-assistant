# ⚡ AI-Powered Executive Email Assistant

An intelligent backend system that connects to Gmail and uses **Google Gemini 2.0 Flash** to automatically classify emails by intent, extract key details, and present them in a structured Streamlit dashboard — turning a cluttered inbox into a clean action list.

---

## What It Does

- Connects to Gmail via OAuth 2.0 and fetches real emails
- Classifies each email into `SCHEDULING` (meetings/appointments) or `UPDATE` (status reports/info)
- Extracts structured data — meeting times, participants, summaries — as JSON
- Handles complex Multipart MIME (HTML + Plain Text) email formats
- Displays everything in a clean Streamlit dashboard with client-side caching to manage API rate limits

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| AI Engine | Google Gemini 2.0 Flash |
| Dashboard | Streamlit |
| Email API | Google Gmail API |
| Auth | OAuth 2.0 + Google Auth |
| Config | Dotenv (secrets management) |

---

## Project Structure

```
ai-email-assistant/
├── src/
│   ├── agent.py           # Gemini AI logic + prompt engineering
│   └── gmail_service.py   # Gmail API integration + MIME parsing
├── dashboard.py           # Streamlit UI + caching layer
├── auth_setup.py          # OAuth 2.0 setup script
├── requirements.txt
└── .env                   # API keys (local only, excluded from git)
```

---

## Setup & Run

```bash
git clone https://github.com/Siddhimudgal1417/ai-email-assistant.git
cd ai-email-assistant

pip install -r requirements.txt

# Add your credentials to .env
# GEMINI_API_KEY=your_key
# Run OAuth setup (creates credentials.json)
python auth_setup.py

# Launch dashboard
streamlit run dashboard.py
```

---

## Key Features

- 🤖 LLM-powered intent classification (SCHEDULING vs UPDATE)
- 📧 Full Gmail API integration with OAuth 2.0
- 🧩 Multipart MIME email parsing (HTML + plain text)
- ⚡ Client-side caching to manage Gemini API rate limits
- 📋 Structured JSON extraction — meeting time, participants, summary
- 🔐 Strict environment variable management — no secrets in code

---

## Skills Demonstrated

`Python` `Google Gemini API` `Gmail API` `OAuth 2.0` `Streamlit` `Prompt Engineering` `MIME Parsing` `LLM Orchestration`

---

**Author:** Siddhi Mudgal · [LinkedIn](https://linkedin.com/in/https://www.linkedin.com/in/siddhi-mudgal/) · [GitHub](https://github.com/Siddhimudgal1417)
