# System Architecture: Multi-Agent Weekly App Reviews Pulse for Groww

## 1. System Overview
The system automates the ingestion, analysis, and summarization of app store reviews for the **Groww** application. It leverages **Groq** for high-speed inference and **MCP (Model Context Protocol)** for external integrations. The system features a "Human-in-the-Loop" workflow via a **Streamlit** frontend. 

Crucially, the system bypasses local file storage for deliverables, instead utilizing **Google Docs** and **Google Drive** via MCP to ensure professional, cloud-based organization.

## 2. High-Level Multi-Agent Architecture

```mermaid
graph LR
    %%{init: {'theme': 'default', 'themeVariables': { 'fontSize': '16px', 'fontFamily': 'arial'}}}%%
    
    subgraph ToolingLayer [Tooling Layer MCP]
        AppStore[App/Play Store MCP Server]
        Gmail[Gmail / Email MCP Server]
        GoogleDocs[Google Docs MCP Server]
        GoogleDrive[Google Drive MCP Server]
    end

    subgraph LLMEngine [LLM Engine]
        Groq[Groq Inference API]
    end

    subgraph MultiAgentSystem [Multi-Agent System]
        Orchestrator{Orchestrator}
        Analyst(Data Analyst Agent)
        PM(Product Manager Agent)
        Writer(Copywriter Agent)
        Reviewer(Reviewer Agent)
    end
    
    subgraph FrontendUI [Streamlit Dashboard]
        WebUI[User Interface]
        Approval{Human Approval?}
    end

    WebUI -->|1. Start| Orchestrator
    Groq -.-> Orchestrator
    
    AppStore -->|2. Raw Reviews| Analyst
    Orchestrator --> Analyst
    Analyst -->|3. Themes & Quotes| Orchestrator
    
    Orchestrator --> PM
    PM -->|4. Ideas| Orchestrator
    
    Orchestrator --> Writer
    Writer -->|5. Draft Note| Orchestrator
    
    Orchestrator --> Reviewer
    Reviewer -->|6a. Revisions| Writer
    Reviewer -->|6b. Final Version| Orchestrator
    
    Orchestrator -->|7. Display Preview| WebUI
    WebUI --> Approval
    
    Approval -->|8. Push Deliverables| GoogleDocs
    Approval -->|8. Push Deliverables| GoogleDrive
    Approval -->|8. Push Deliverables| Gmail
    
    GoogleDocs -->|Output| Doc[Google Doc Note]
    GoogleDrive -->|Output| CSV[Sanitized CSV]
    Gmail -->|Output| Draft[Email Draft]
```

## 3. The "Human-in-the-Loop" Frontend
- **Live Agent Feed:** Visual log of agent collaboration.
- **Approval Gate:** The system pauses for human review.
- **One-Click Distribution:** Upon approval, the system simultaneously creates a **Google Doc**, uploads the **Sanitized CSV** to Google Drive, and creates a **Gmail Draft**.

## 4. Strict Compliance & Constraints Matrix
1. **No Behind-Login Scraping:** Uses only public review feeds.
2. **Zero PII:** Scrubbed via regex/NLP before entering LLM.
3. **Max 5 Themes:** Enforced by Analyst prompt.
4. **Scannability (≤250 words):** Enforced by Reviewer loop.

## 5. Tool Integration via MCP
- **`mcp-server-app-store`:** Fetches real-time public reviews.
- **`mcp-server-gmail`:** Creates the draft.
- **`mcp-server-google-docs`:** Creates the official one-page weekly note deliverable.
- **`mcp-server-google-drive`:** Stores the sanitized CSV dataset.

## 6. Deployment & Tech Stack
- **Framework:** Pure Python Orchestration (utilizing a stateful `GrowwPulseOrchestrator` class).
- **Brain:** Groq.
- **UI:** Streamlit.
- **Hosting:** Render.

## 7. Agent Roles
(Unchanged roles: Orchestrator, Analyst, PM, Writer, Reviewer)
