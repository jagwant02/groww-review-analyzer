# Detailed Implementation Plan: Groww Weekly Pulse Multi-Agent System

This document outlines the phase-wise implementation plan for building the AI-powered weekly app reviews pulse system for Groww.

## Phase 1: Environment Setup & Data Ingestion 
**Goal:** Establish foundational tools, connect to data sources, and implement strict PII sanitization.

1. **Repository Setup:**
   - Initialize GitHub repository and virtual environment.
   - Install dependencies: `google-play-scraper`, `pandas`, `groq`, `langgraph`, `streamlit`.
2. **Data Fetching (Google Play):**
   - Implement `src/fetch_reviews.py` to pull 200 newest reviews for Groww (`com.nextbillion.groww`).
3. **PII Sanitization:**
   - Implement `src/sanitize.py` to strip Emails, Phone Numbers, and IDs.
   - Drop the `userName` column for 100% compliance.

## Phase 2: Agent Development & Orchestration (Detailed)
**Goal:** Build the individual agents and a pure Python stateful orchestrator class.

1. **State Definition:** Define a shared dictionary or class state (raw_reviews, themes, quotes, actionable_ideas, draft_note, review_status, feedback).
2. **Agent Construction:**
   - **Analyst:** Max 5 themes, 3 quotes.
   - **PM:** 3 actionable ideas.
   - **Writer:** Combined markdown note, strictly < 250 words.
   - **Reviewer:** Verification logic with a loop back to Writer if word count or PII checks fail.
3. **Orchestrator Logic:**
   - Implement a `GrowwPulseOrchestrator` class to manage the sequence and the 3-iteration loop.

## Phase 3: "Human-in-the-Loop" Streamlit Frontend
**Goal:** Create the LinkedIn-ready dashboard to trigger and approve the workflow.

1. **UI Layout:** Dashboard with "Start Analysis" and "Review/Approve" components.
2. **Live Monitoring:** Display real-time logs from the execution.
3. **Approval Logic:** Once approved, trigger the **Phase 4** multi-platform distribution.

## Phase 4: Google Workspace Distribution & Deployment
**Goal:** Connect to Gmail, Google Docs, and Google Drive via MCP.

1. **Google Cloud Setup:**
   - Enable Gmail, Google Docs, and Google Drive APIs.
   - Setup OAuth 2.0 credentials for MCP servers.
2. **MCP Deliverables Integration:**
   - **Google Docs:** Create a new doc with the title "Groww Weekly Pulse - [Date]" and paste the approved note.
   - **Google Drive:** Upload the `scrubbed_reviews.csv` to a designated "M4 Deliverables" folder.
   - **Gmail:** Create a draft in the user's inbox with the note content.
3. **Deployment:**
   - Deploy to **Render** as a single Python service hosting the Streamlit app and MCP clients.

---

> [!IMPORTANT]
> **User Review Required:** The plan now reflects **Google Docs/Drive** as the primary storage for deliverables to match the problem statement requirements. Do you approve this updated implementation path?
