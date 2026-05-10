# 📈 Groww Weekly Pulse Generator

A multi-agent AI system that turns Groww's Play Store reviews into a one-page weekly brief — themes, user quotes, and product action ideas — delivered automatically to Google Docs and Gmail.

---

## The Problem

PM teams get hundreds of app reviews every week. Reading them manually is slow and inconsistent. Insights sit unread, patterns get missed, and roadmap decisions get made without the full picture of what users are actually saying.

---

## How It Works

```
Play Store Reviews
       ↓
Analyst Agent       → top 5 themes + 3 real user quotes
       ↓
PM Agent            → 3 actionable product ideas
       ↓
Copywriter Agent    → clean <250 word pulse note
       ↓
Reviewer Agent      → checks compliance + word count (loops back if needed)
       ↓
Streamlit Dashboard → human approves before anything goes out
       ↓
Google Docs · Google Drive · Gmail
```

---

## Key Product Decisions

**Human-in-the-loop before publishing** — AI-generated insights going straight to a leadership inbox without review is a reliability risk. The approval gate is a deliberate product choice, not a technical limitation.

**Self-correcting Reviewer agent** — instead of hardcoding rules, a dedicated agent checks the output and sends it back if it fails. Self-correcting, not brittle.

**PII scrubbed before the LLM sees anything** — names, emails, and phone numbers stripped at ingestion. The LLM never touches personal data.

**Output goes to Google Workspace** — PMs already live in Docs and Gmail. No new tool to adopt, no friction.

---

## Tech Stack
Python · Groq (Llama 3) · Streamlit · Google Docs API · Google Drive API · Gmail API · Render

---

## What I'd Build Next
- Sentiment trend tracking week-over-week
- Multi-app support to monitor competitors alongside Groww
- Slack integration for channel delivery
- Automated theme scoring by frequency and severity

---

*Built by Jagwant Singh · [LinkedIn](https://linkedin.com/in/jagwant-singh01)*
