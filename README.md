# 📈 Groww Weekly Pulse Generator

An AI-powered system that automates the collection, sanitization, and analysis of Groww app reviews using a multi-agent approach. 

## 🚀 Key Features
- **Data Ingestion:** Automatically fetches public reviews for Groww from the Google Play Store.
- **Privacy First:** Strict PII scrubbing removing names, emails, and phone numbers.
- **Multi-Agent Analysis:**
  - **Analyst:** Extracts top 5 themes and 3 quotes.
  - **Product Manager:** Generates 3 actionable roadmap ideas.
  - **Copywriter:** Drafts a <250 word Markdown note.
  - **Reviewer:** Self-correcting QA loop to ensure word counts and compliance.
- **Human-in-the-Loop:** Streamlit dashboard for real-time monitoring and approval.
- **Google Workspace Sync:** One-click publishing to Google Docs, Google Drive, and Gmail.

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Groq API Key (from [console.groq.com](https://console.groq.com/))
- Google Cloud Project with Gmail, Google Docs, and Google Drive APIs enabled.

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```text
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Google Workspace Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable **Gmail API**, **Google Docs API**, and **Google Drive API**.
3. Create an **OAuth 2.0 Client ID** (Desktop App).
4. Download the JSON file and rename it to `credentials.json` in the project root.

### 5. Running the App
```bash
streamlit run app.py
```

## 📦 Deliverables
Upon clicking "Approve" in the dashboard:
1. **Google Doc:** A professional one-page weekly note.
2. **Google Drive:** The sanitized reviews CSV dataset.
3. **Gmail:** A draft email containing the pulse note.

## 📄 License
MIT
